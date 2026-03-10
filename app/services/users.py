"""
The Cache-Aside pattern (or lazy loading) is a caching strategy where the application
code manages data flow between the database and the cache. The app checks the cache
first; on a miss, it fetches from the database, updates the cache, and returns the
data, reducing database load and improving read performance


1.- The application determines whether an item currently resides in the cache by
attempting to read from the cache.

2.- If the item isn't in the cache, also known as a cache miss, the application
retrieves the item from the data store.

3.- The application adds the item to the cache and then returns it to the caller.

If an application updates information, it can follow the write-through strategy
by making the modification to the data store and invalidating the corresponding
item in the cache.

When the item is needed again, the Cache-Aside pattern retrieves the updated data
from the data store and adds it to the cache.
"""

import json
from fastapi import HTTPException, status

from app.core.dependencies import RedisDep, SessionDep
from app.models import User
from app.schemas import UserCreate, UserUpdate

CACHE_TTL = 60


class UserService:
    @staticmethod
    async def create(db: SessionDep, data: UserCreate) -> User:
        user = User(name=data.name, email=data.email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def get_cached(db: SessionDep, redis: RedisDep, user_id: int) -> User:
        """
        The Cache-Aside pattern relies on this cycle of serialization (Object → String) and deserialization (String → Object).
        """
        cache_key = f"user:{user_id}"

        # 1️⃣ Check cache
        cached = await redis.get(cache_key)
        if cached:
            return User(**json.loads(cached))

        # 2️⃣ Fetch from DB
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(404, "User not found")

        # 3️⃣ Populate cache
        await redis.setex(cache_key, CACHE_TTL, user.model_dump_json())

        return user

    @staticmethod
    async def update(db: SessionDep, redis, user_id: int, data: UserUpdate) -> User:

        user = await db.get(User, user_id)
        if not user:
            # raise UserNotFoundException(user_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exits"
            )
        user_data_update = data.model_dump(exclude_unset=True)
        for key, value in user_data_update.items():
            setattr(user, key, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user
