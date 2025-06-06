from pydantic import BaseModel
from datetime import datetime

class PasteCreate(BaseModel):
    content: str
    expiration: str
    language: str

class Paste(BaseModel):
    id: str
    content: str
    language: str
    created_at: datetime
    expiration: str
    views: int
    is_active: bool

    class Config:
        orm_mode = True
        from_attributes = True