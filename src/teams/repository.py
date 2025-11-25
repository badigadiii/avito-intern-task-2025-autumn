from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.teams.exceptions import TeamMemberAlreadyHaveTeam
from src.teams.models import Teams, TeamMembers
from src.teams.schemas import TeamMemberCreate, TeamMember
from src.users.models import Users


class TeamsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_team_by_id(self, id: int) -> Teams | None:
        stmt = select(Teams).where(Teams.id == id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_team_by_name(self, name: str) -> Teams | None:
        stmt = select(Teams).where(Teams.name == name)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_team_by_user_id(self, user_id: str) -> Teams | None:
        stmt = select(Teams).where(
            Teams.id.in_(
                select(TeamMembers.team_id).where(TeamMembers.user_id == user_id)
            )
        )
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_team(self, name: str) -> Teams | None:
        team = Teams(name=name)
        self.db.add(team)

    async def _user_already_have_team(self, user_id: str):
        stmt = select(TeamMembers).where(TeamMembers.user_id == user_id)
        result = await self.db.execute(stmt)

        return bool(result.first())

    async def add_team_member(
        self, team_name: str, member: TeamMemberCreate
    ) -> TeamMember | None:
        team = await self.get_team_by_name(team_name)

        if self._user_already_have_team(member.user_id):
            raise TeamMemberAlreadyHaveTeam(member.user_id)

        if team:
            team_member = TeamMembers(user_id=member.user_id, team_id=team.id)
            self.db.add(team_member)

            return TeamMember(
                user_id=member.user_id,
                username=member.username,
                is_active=member.is_active,
            )
        return None

    async def get_team_members(self, team_name: str) -> list[Users]:
        team = await self.get_team_by_name(team_name)

        stmt = (
            select(Users)
            .join(TeamMembers, TeamMembers.user_id == Users.id)
            .where(TeamMembers.team_id == team.id)
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()
