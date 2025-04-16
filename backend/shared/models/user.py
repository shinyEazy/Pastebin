from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from shared.database import Base
from datetime import datetime
import pytz
from uuid6 import uuid7

local_tz = pytz.timezone("Asia/Bangkok")

class User(Base):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid7()))
    username = Column(String(36), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(local_tz))
    total_pastes = Column(Integer, default=0)
    pastes = relationship("Paste", back_populates="user")