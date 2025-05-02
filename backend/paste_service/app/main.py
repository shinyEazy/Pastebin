from fastapi import FastAPI
from shared.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pastes
from shared.models.user import User 
from app.utils import cleanup_expired_pastes
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager
import threading
import time
from typing import List
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from app.crud import batch_worker, process_batch

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        cleanup_expired_pastes,
        trigger=IntervalTrigger(hours=10),
        max_instances=1
    )
    
    scheduler.add_job(
        process_batch,
        trigger=IntervalTrigger(minutes=1),
        max_instances=1
    )
    
    scheduler.start()
    
    logger.info("Application started with batch processing enabled")
    
    yield
    
    logger.info("Shutting down application")
    scheduler.shutdown()
    
    process_batch()

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pastes.router)