from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: str
    username: str
    created_at: datetime
    total_pastes: int

    class Config:
        orm_mode = True
        from_attributes = True