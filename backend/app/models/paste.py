from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base  
import pytz

local_tz = pytz.timezone("Asia/Bangkok")  

class Paste(Base):
    __tablename__ = "pastes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(local_tz))
    expire_at = Column(DateTime, nullable=True)