import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.db_helper import DbDep
from src.schemas.enums import ErrorCode
from src.teams.repository import TeamsRepository
from src.teams.schemas import (
    TeamResponse,
    TeamCreate,
    TeamMemberBase,
    TeamQuery,
    TeamMember,
    TeamMemberCreate,
)


class TeamsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TeamsRepository(db)

    def _clean_duplicated_team_members(
        self, team_members: list[TeamMemberCreate]
    ) -> list[TeamMemberBase]:
        seen: set[uuid.UUID] = set()
        cleaned: list[TeamMemberBase] = []

        for member in team_members:
            if member.user_id not in seen:
                seen.add(member.user_id)
                cleaned.append(
                    TeamMemberBase(
                        user_id=member.user_id,
                        username=member.username,
                        is_active=member.is_active,
                    )
                )

        return cleaned

    async def create_team(self, team: TeamCreate) -> TeamResponse:
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

        await self.repo.create_team(team.team_name)

        created_members: list[TeamMemberBase] = []
        team_members = self._clean_duplicated_team_members(team.members)

        for member in team_members:
            created_member = await self.repo.add_team_member(team.team_name, member)
            if created_member:
                created_members.append(created_member)

        await self.db.commit()

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
