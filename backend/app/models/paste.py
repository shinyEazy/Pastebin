from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from app.database import Base  
import pytz
import uuid

local_tz = pytz.timezone("Asia/Bangkok")  
        
class Paste(Base):
    __tablename__ = "pastes"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    content = Column(Text, nullable=False)
    language = Column(String(50), default="plaintext")
    created_at = Column(DateTime, default=lambda: datetime.now(local_tz))
    expiration = Column(String(50), default="Never")
    views = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)