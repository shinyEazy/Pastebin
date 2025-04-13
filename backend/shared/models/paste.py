from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from shared.database import Base
from datetime import datetime
import pytz
from uuid6 import uuid7

local_tz = pytz.timezone("Asia/Bangkok")

class Paste(Base):
    __tablename__ = "pastes"
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid7()))
    content = Column(Text, nullable=False)
    language = Column(String(50), default="plaintext")
    created_at = Column(DateTime, default=lambda: datetime.now(local_tz))
    expiration = Column(String(50), default="Never")
    views = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)