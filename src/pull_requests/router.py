from fastapi import APIRouter, Depends

from src.pull_requests.schemas import (
    PullRequestCreate,
    PullRequestMerge,
    PullRequestReassign,
    PullRequestResponse,
    PullRequestReassignResponse,
)
from src.pull_requests.service import PullRequestsService, get_pull_requests_service

router = APIRouter()


@router.post("/create", response_model_exclude_none=True)
async def create_pull_request(
    pr: PullRequestCreate,
    pr_service: PullRequestsService = Depends(get_pull_requests_service),
) -> PullRequestResponse:
    return await pr_service.create_pull_request(pr)


@router.post("/reassign", response_model_exclude_none=True)
async def reassign_pull_request(
    pr: PullRequestReassign,
    pr_service: PullRequestsService = Depends(get_pull_requests_service),
) -> PullRequestReassignResponse:
    return await pr_service.reassign_reviewers(pr)


@router.post("/merge", response_model_exclude_none=True)
async def merge_pull_request(
    pr: PullRequestMerge,
    pr_service: PullRequestsService = Depends(get_pull_requests_service),
) -> PullRequestResponse:
    pass
