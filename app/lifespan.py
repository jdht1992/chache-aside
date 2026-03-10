from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_all_tables
from app.core.redis import create_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    app.state.redis = await create_redis()
    yield
    await app.state.redis.close()
