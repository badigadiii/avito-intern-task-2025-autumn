from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import PullRequests, Users, PullRequestsReviewers
from src.pull_requests.exceptions import PullRequestAlreadyExists
from src.teams.repository import TeamsRepository


class PullRequestsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.teams_repo = TeamsRepository(db)

    async def _is_pr_already_exists(self, pull_request_id: str) -> bool:
        stmt = select(PullRequests).where(PullRequests.id == pull_request_id)
        result = await self.db.execute(stmt)

        return bool(result.scalar_one_or_none())

    async def create_pull_request(
        self, pull_request_id: str, pull_request_name: str, author_id: str
    ) -> PullRequests | None:
        if self._is_pr_already_exists(pull_request_id):
            raise PullRequestAlreadyExists(pull_request_id=pull_request_id)

        pr = PullRequests(
            id=pull_request_id,
            author_id=author_id,
            pull_request_name=pull_request_name,
        )
        self.db.add(pr)

        return pr

    async def get_team_members_to_assign_review(
        self, team_id: int, *users_ids_to_exclude: str
    ) -> list[Users]:
        team_members = await self.teams_repo.get_team_members_by_team_id(
            team_id=team_id
        )
        team_members = [
            member
            for member in team_members
            if member.id not in users_ids_to_exclude and member.is_active
        ]

        return team_members

    async def assign_reviewers(self, pull_request_id: str, reviewers: list[Users]):
        for reviewer in reviewers:
            pr_reviewer = PullRequestsReviewers(
                reviewer_id=reviewer.id, pull_request_id=pull_request_id
            )
            self.db.add(pr_reviewer)
