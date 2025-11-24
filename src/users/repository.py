from sqlalchemy.ext.asyncio import AsyncSession

from src.users.model import Users


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str):
        user = Users(username=username)
        self.db.add(user)
        await self.db.commit()
