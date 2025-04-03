from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from shared.database import Base
from datetime import datetime
import pytz

local_tz = pytz.timezone("Asia/Bangkok")

class Paste(Base):
    __tablename__ = "pastes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    language = Column(String(50), default="plaintext")
    created_at = Column(DateTime, default=lambda: datetime.now(local_tz))
    expiration = Column(String(50), default="Never")
    views = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)