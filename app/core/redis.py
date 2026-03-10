import redis.asyncio as redis
from app.core.config import settings


async def create_redis() -> redis.Redis:
    pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL, decode_responses=True, max_connections=5
    )
    return redis.Redis(connection_pool=pool)
