from fastapi import APIRouter, Depends
from starlette import status

from src.pull_requests.service import get_pull_requests_service, PullRequestsService
from src.users.schemas import (
    UserSetIsActiveSchema,
    UserResponse,
    UserReviewsResponse,
    UserReviewsQuery,
)
from src.users.service import UsersService, get_users_service

router = APIRouter()


@router.post("/setIsActive", status_code=status.HTTP_200_OK)
async def set_is_active(
    user: UserSetIsActiveSchema,
    users_service: UsersService = Depends(get_users_service),
) -> UserResponse:
    return await users_service.set_is_active(user)


@router.get("/getReview")
async def get_review(
    user_reviews_query: UserReviewsQuery,
    pr_service: PullRequestsService = Depends(get_pull_requests_service),
) -> UserReviewsResponse:
    return await pr_service.get_pull_request_reviews(user_reviews_query)
