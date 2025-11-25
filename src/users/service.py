from fastapi import HTTPException
from starlette import status

from src.schemas.enums import ErrorCode
from src.teams.repository import TeamsRepository
from src.users.repository import UsersRepository
from src.db.db_helper import DbDep

from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserSetIsActiveSchema, UserResponse


class UsersService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users_repo = UsersRepository(db)
        self.teams_repo = TeamsRepository(db)

    async def set_is_active(self, user: UserSetIsActiveSchema):
        user = await self.users_repo.update_is_active(user_id=user.user_id, is_active=user.is_active)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NOT_FOUND.name,
                        "message": ErrorCode.NOT_FOUND.value,
                    }
                },
            )

        user_team = await self.teams_repo.get_team_by_user_id(user.id)
        team_name = None if not user_team else user_team.name

        return UserResponse(
            user_id=user.id,
            username=user.username,
            is_active=user.is_active,
            team_name=team_name
        )

    async def get_reviews(self):
        pass


def get_users_service(db: DbDep):
    return UsersService(db)
