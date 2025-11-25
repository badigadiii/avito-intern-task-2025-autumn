from pydantic import BaseModel

from src.pull_requests.schemas import PullRequestShort


class User(BaseModel):
    user_id: str
    username: str
    team_name: str | None
    is_active: bool


class UserSetIsActiveSchema(BaseModel):
    user_id: str
    is_active: bool


class UserResponse(User):
    pass


class UserReviewsQuery(BaseModel):
    user_id: str

class UserReviewsResponse(BaseModel):
    user_id: str
    pull_requests: list[PullRequestShort]
