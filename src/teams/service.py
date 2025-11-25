import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.db_helper import DbDep
from src.schemas.enums import ErrorCode
from src.teams.exceptions import TeamMemberAlreadyHaveTeam
from src.teams.repository import TeamsRepository
from src.teams.schemas import (
    TeamResponse,
    TeamCreate,
    TeamQuery,
    TeamMember,
)
from src.users.repository import UsersRepository


class TeamsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TeamsRepository(db)
        self.users_repo = UsersRepository(db)

    async def create_team(self, team: TeamCreate) -> TeamResponse:
        if len(team.members) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": {
                        "code": ErrorCode.EMPTY_TEAM.name,
                        "message": ErrorCode.EMPTY_TEAM.value,
                    }
                },
            )

        existed_team = await self.repo.get_team_by_name(team.team_name)

        if existed_team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": {
                        "code": ErrorCode.TEAM_EXISTS.name,
                        "message": ErrorCode.TEAM_EXISTS.value,
                    }
                },
            )

        created_members: list[TeamMember] = []

        try:
            await self.repo.create_team(team.team_name)

            for member in team.members:
                await self.users_repo.create_update_user(
                    user_id=member.user_id, username=member.username
                )
                created_member = await self.repo.add_team_member(team.team_name, member)
                if created_member:
                    created_members.append(created_member)

            await self.db.commit()
        except TeamMemberAlreadyHaveTeam as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error": {
                        "message": f"Can't create team, Exception: {e}",
                    }
                },
            )
        except Exception as e:
            logging.error(f"Exception while creating team: {e}")
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error": {
                        "message": f"Exception while creating team: {e}",
                    }
                },
            )

        return TeamResponse(team_name=team.team_name, members=created_members)

    async def get_team_members(self, team: TeamQuery) -> TeamResponse:
        existing_team = await self.repo.get_team_by_name(team.team_name)

        if not existing_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NOT_FOUND.name,
                        "message": ErrorCode.NOT_FOUND.value,
                    }
                },
            )

        team_members = await self.repo.get_team_members(team.team_name)
        team_members = [
            TeamMember(
                user_id=str(team_member.id),
                username=team_member.username,
                is_active=team_member.is_active,
            )
            for team_member in team_members
        ]

        return TeamResponse(team_name=team.team_name, members=team_members)


def get_teams_service(db: DbDep) -> TeamsService:
    return TeamsService(db)
