from fastapi import FastAPI
from shared.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.routes import pastes


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pastes.router, prefix="/api")