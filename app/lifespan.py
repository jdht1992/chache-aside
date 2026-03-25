from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.redis import create_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await create_redis()
    yield
    await app.state.redis.close()
