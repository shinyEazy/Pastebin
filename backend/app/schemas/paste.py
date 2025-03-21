from datetime import datetime
from pydantic import BaseModel

class PasteCreate(BaseModel):
    content: str
    expiration: str

class Paste(BaseModel):
    id: int
    content: str
    created_at: datetime
    expiration: str 
    views: int
    is_active: bool

    class Config:
        orm_mode = True