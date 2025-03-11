from datetime import datetime
from pydantic import BaseModel

class PasteCreate(BaseModel):
    content: str
    expire_at: datetime | None = None

class Paste(BaseModel):
    id: int
    content: str
    created_at: datetime
    expire_at: datetime | None

    class Config:
        orm_mode = True