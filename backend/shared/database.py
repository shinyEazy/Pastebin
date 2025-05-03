from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from shared.config import settings

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Optimize connection pool settings for high concurrency
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,                    # Increase from default
    max_overflow=30,                 # Allow more connections when under pressure
    pool_timeout=30,                 # Wait longer for a connection when busy
    pool_recycle=1800,               # Recycle connections every 30 minutes
    pool_pre_ping=True,              # Test connections before use to prevent stale connections
    echo=False                       # Turn off SQL echoing in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()