from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from shared.database import Base, engine
from app.crud import process_batch
from app.routes import pastes
# from shared.utils import cleanup_expired_pastes

# Configure proper origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # Add additional origins as needed
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a more efficient scheduler
    scheduler = BackgroundScheduler(
        job_defaults={"coalesce": True, "max_instances": 1}
    )

    # Run cleanup less frequently (not needed every few minutes)
    # scheduler.add_job(
    #     cleanup_expired_pastes,
    #     trigger=IntervalTrigger(hours=24),  # Run once a day
    #     max_instances=1
    # )

    # Stagger batch processing to avoid all workers running simultaneously
    for i in range(4):
        scheduler.add_job(
            lambda worker_id=i: process_batch(worker_id),
            trigger=IntervalTrigger(seconds=60 + (i * 15)),  # Stagger by 15 seconds
            max_instances=1
        )

    scheduler.start()
    yield
    scheduler.shutdown()

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure FastAPI with optimized settings
app = FastAPI(
    lifespan=lifespan,
)

# Properly configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    # Add cache headers for OPTIONS requests
    expose_headers=["X-Process-Time", "X-Rate-Limit"]
)
app.include_router(pastes.router)