from fastapi import FastAPI
from app.routes import pastes
from app.database import Base, engine  
from fastapi.middleware.cors import CORSMiddleware
from app.background import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pastes.router, prefix="/api")