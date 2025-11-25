from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class PullRequestStatus(str, Enum):
    OPEN = "open"
    MERGED = "merged"


class PullRequestBase(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PullRequestStatus


class PullRequest(PullRequestBase):
    assigned_reviewers: list[str]
    createdAt: datetime | None = None
    mergedAt: datetime | None = None


class PullRequestShort(PullRequestBase):
    pass


class PullRequestCreate(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str


class PullRequestMerge(BaseModel):
    pull_request_id: str


class PullRequestReassign(BaseModel):
    pull_request_id: str
    old_user_id: str


class PullRequestResponse(BaseModel):
    pr: PullRequest


class PullRequestReassignResponse(BaseModel):
    pr: PullRequest
    replaced_by: str
