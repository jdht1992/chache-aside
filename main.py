from fastapi import FastAPI

from app.lifespan import lifespan
from app.routers.users import router as users_router

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
