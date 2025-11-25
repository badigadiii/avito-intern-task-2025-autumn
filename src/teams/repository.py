from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.teams.models import Teams, TeamMembers
from src.teams.schemas import TeamMemberCreate, TeamMember
from src.users.models import Users
from src.users.repository import UsersRepository


class TeamsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users_repo = UsersRepository(db)

    async def get_team_by_id(self, id: int) -> Teams | None:
        stmt = select(Teams).where(Teams.id == id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_team_by_name(self, name: str) -> Teams | None:
        stmt = select(Teams).where(Teams.name == name)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_team(self, name: str) -> Teams | None:
        team = Teams(name=name)
        self.db.add(team)

    async def add_team_member(
        self, team_name: str, member: TeamMemberCreate
    ) -> TeamMember | None:
        team = await self.get_team_by_name(team_name)

        if team:
            team_member = TeamMembers(user_id=member.user_id, team_id=team.id)
            self.db.add(team_member)

            return TeamMember(
                user_id=member.user_id,
                username=member.username,
                is_active=member.is_active
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
