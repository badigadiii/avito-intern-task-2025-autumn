import random

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src import Users
from src.db.db_helper import DbDep
from src.pull_requests.exceptions import PullRequestAlreadyExists
from src.pull_requests.repository import PullRequestsRepository
from src.pull_requests.schemas import (
    PullRequestCreate,
    PullRequestResponse,
    PullRequest,
    PullRequestReassign,
    PullRequestShort,
    PullRequestReassignResponse,
    PullRequestStatus,
    PullRequestMerge,
    PullRequestMergedResponse,
)
from src.schemas.enums import ErrorCode
from src.teams.repository import TeamsRepository
from src.users.schemas import UserReviewsResponse, UserReviewsQuery


class PullRequestsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = PullRequestsRepository(db)
        self.teams_repo = TeamsRepository(db)

    async def create_pull_request(self, pr: PullRequestCreate) -> PullRequestResponse:
        try:
            created_pr = await self.repo.create_pull_request(
                pull_request_id=pr.pull_request_id,
                author_id=pr.author_id,
                pull_request_name=pr.pull_request_name,
            )
        except PullRequestAlreadyExists:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {
                        "code": ErrorCode.PR_EXISTS.name,
                        "message": ErrorCode.PR_EXISTS.value,
                    }
                },
            )

        team = await self.teams_repo.get_team_by_user_id(pr.author_id)

        if not team:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NOT_FOUND.name,
                        "message": ErrorCode.NOT_FOUND.value,
                    }
                },
            )

        potential_reviewers = await self.repo.get_team_members_to_assign_review(
            team.id, pr.author_id
        )

        if potential_reviewers:
            potential_reviewers = list(potential_reviewers)[:2]
            await self.repo.assign_reviewers(pr.pull_request_id, potential_reviewers)
            await self.db.commit()

            assigned_reviewers = [reviewer.id for reviewer in potential_reviewers]

            return PullRequestResponse(
                pr=PullRequest(
                    pull_request_id=pr.pull_request_id,
                    pull_request_name=pr.pull_request_name,
                    author_id=pr.author_id,
                    status=created_pr.status,
                    assigned_reviewers=assigned_reviewers,
                )
            )

        await self.db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": ErrorCode.NOT_FOUND.name,
                    "message": ErrorCode.NOT_FOUND.value,
                }
            },
        )

    async def get_pull_request_reviews(self, user_reviews_query: UserReviewsQuery) -> UserReviewsResponse:
        reviews = await self.repo.get_user_reviews(user_reviews_query.user_id)
        pull_requests = [
            PullRequestShort(
                pull_request_id=pr.id,
                pull_request_name=pr.pull_request_name,
                author_id=pr.author_id,
                status=pr.status
            )
            for pr in reviews
        ]
        return UserReviewsResponse(
            user_id=user_reviews_query.user_id,
            pull_requests=pull_requests
        )

    async def reassign_reviewers(self, pr: PullRequestReassign) -> PullRequestReassignResponse:
        old_reviewer = await self.repo.get_reviewer(pr.pull_request_id, pr.old_user_id)
        pull_request = await self.repo.get_pull_request_by_id(pr.pull_request_id)

        if not pull_request or not old_reviewer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NOT_FOUND.name,
                        "message": ErrorCode.NOT_FOUND.value,
                    }
                },
            )

        if pull_request.status == PullRequestStatus.MERGED:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {
                        "code": ErrorCode.PR_MERGED.name,
                        "message": ErrorCode.PR_MERGED.value,
                    }
                },
            )

        old_reviewer_team = await self.teams_repo.get_team_by_user_id(pr.old_user_id)
        potential_reviewers = await self.repo.get_team_members_to_assign_review(
            old_reviewer_team.id,
            old_reviewer.reviewer_id, pull_request.author_id
        )

        if potential_reviewers:
            new_reviewer: Users = random.choice(potential_reviewers)
            old_reviewer.reviewer_id = new_reviewer.id

            await self.db.commit()

            current_reviewers = await self.repo.get_reviewers_by_pull_request_id(pr.pull_request_id)
            current_reviewers = [reviewer.id for reviewer in current_reviewers]

            return PullRequestReassignResponse(
                pr=PullRequest(
                    pull_request_id=pull_request.id,
                    pull_request_name=pull_request.pull_request_name,
                    author_id=pull_request.author_id,
                    status=pull_request.status,
                    assigned_reviewers=current_reviewers
                ),
                replaced_by=old_reviewer.reviewer_id
            )
        else:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NO_CANDIDATE.name,
                        "message": ErrorCode.NO_CANDIDATE.value,
                    }
                },
            )

    async def merge_pull_request(self, pr: PullRequestMerge) -> PullRequestMergedResponse:
        pull_request = await self.repo.merge_pull_request(pr.pull_request_id)

        if not pull_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": {
                        "code": ErrorCode.NOT_FOUND.name,
                        "message": ErrorCode.NOT_FOUND.value,
                    }
                },
            )

        current_reviewers = await self.repo.get_reviewers_by_pull_request_id(pr.pull_request_id)
        current_reviewers = [reviewer.id for reviewer in current_reviewers]

        return PullRequestMergedResponse(
            pr=PullRequest(
                pull_request_id=pull_request.id,
                pull_request_name=pull_request.pull_request_name,
                author_id=pull_request.author_id,
                status=pull_request.status,
                assigned_reviewers=current_reviewers
            ),
            mergedAt=pull_request.merged_at
        )



def get_pull_requests_service(db: DbDep):
    return PullRequestsService(db)
