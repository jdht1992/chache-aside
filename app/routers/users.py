from fastapi import APIRouter
from app.core.dependencies import RedisDep, SessionDep
from app.services.users import UserService
from ..schemas import UserCreate, UserUpdate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(data: UserCreate, db: SessionDep):
    return await UserService.create(db, data)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: SessionDep, redis: RedisDep):
    return await UserService.get_cached(db, redis, user_id)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, data: UserUpdate, db: SessionDep, redis: RedisDep):
    return await UserService.update(db, redis, user_id, data)
