import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import Users


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user(self, id: uuid.UUID) -> Users | None:
        stmt = select(Users).where(Users.id == id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_user(self, username: str):
        user = Users(username=username)
        self.db.add(user)
        await self.db.commit()
