from datetime import datetime

from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from src.db.base import Base
from .schemas import PullRequestStatus


class PullRequests(Base):
    __tablename__ = "pull_requests"

    id: Mapped[str] = mapped_column(primary_key=True)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    pull_request_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[PullRequestStatus] = mapped_column(
        pgEnum(
            PullRequestStatus,
            name="pull_request_status_enum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        server_default=PullRequestStatus.OPEN.value,
        nullable=False,
    )
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
    merged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class PullRequestsReviewers(Base):
    __tablename__ = "pull_request_reviewers"

    pull_request_id: Mapped[str] = mapped_column(
        ForeignKey("pull_requests.id", ondelete="CASCADE"), primary_key=True
    )
    reviewer_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
