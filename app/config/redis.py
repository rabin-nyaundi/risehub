from redis import Redis
from app.config.settings import settings

# Create Redis client
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

# Dependency to get Redis client
def get_redis():
    try:
        yield redis_client
    finally:
        redis_client.close()
