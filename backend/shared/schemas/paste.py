from pydantic import BaseModel
from datetime import datetime

class PasteCreate(BaseModel):
    content: str
    expiration: str
    language: str
    
     

class Paste(BaseModel):
    id: int
    content: str
    language: str
    created_at: datetime
    expiration: str
    views: int
    is_active: bool
    # user_id: int


    
   

    class Config:
        orm_mode = True
        from_attributes = True