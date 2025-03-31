from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int = 3306
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()