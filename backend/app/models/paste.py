from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base  # Changed import

class Paste(Base):
    __tablename__ = "pastes"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    language = Column(String(50), nullable=True)
    expire_at = Column(DateTime, nullable=True)