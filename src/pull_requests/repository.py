from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from src import PullRequests, Users, PullRequestsReviewers
from src.pull_requests.exceptions import PullRequestAlreadyExists
from src.teams.repository import TeamsRepository


class PullRequestsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.teams_repo = TeamsRepository(db)

    async def get_pull_request_by_id(self, pull_request_id: str) -> PullRequests | None:
        stmt = select(PullRequests).where(PullRequests.id == pull_request_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create_pull_request(
        self, pull_request_id: str, pull_request_name: str, author_id: str
    ) -> PullRequests | None:
        if self.get_pull_request_by_id(pull_request_id):
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

    async def get_user_reviews(self, user_id: str) -> list[PullRequests]:
        stmt = (
            select(PullRequests)
            .where(PullRequests.id.in_(
                select(PullRequestsReviewers.pull_request_id)
                .where(PullRequestsReviewers.reviewer_id == user_id)
            ))
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()
