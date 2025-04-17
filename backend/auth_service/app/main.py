from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.database import Base, engine
from shared.models.user import User
from shared.models.paste import Paste
from app.routes import auth

# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)