from redis import Redis
from app.config import settings

def get_redis():
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )
    try:
        yield redis_client
    finally:
        redis_client.close()
