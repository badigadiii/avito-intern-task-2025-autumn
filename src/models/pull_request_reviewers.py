from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class PullRequestsReviewers(Base):
    __tablename__ = "pull_request_reviewers"

    pull_request_id: Mapped[int] = mapped_column(
        ForeignKey("pull_requests.id"), primary_key=True
    )
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
