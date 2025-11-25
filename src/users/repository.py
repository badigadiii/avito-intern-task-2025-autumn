from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Users


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, id: str) -> Users | None:
        stmt = select(Users).where(Users.id == id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_update_user(self, user_id: str, username: str) -> Users:
        result = await self.db.execute(select(Users).where(Users.id == user_id))
        user = result.scalar_one_or_none()

        if user:
            user.username = username
        else:
            user = Users(id=user_id, username=username)
            self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_is_active(self, user_id: str, is_active: bool) -> Users | None:
        user = await self.get_user(user_id)

        if not user:
            return None

        user.is_active = is_active

        await self.db.commit()
        await self.db.refresh(user)
        return user
