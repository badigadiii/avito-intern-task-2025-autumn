from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from .base import Base


class PullRequestStatus(Enum):
    OPEN = "open"
    MERGED = "merged"


class PullRequests(Base):
    __tablename__ = "pull_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    pull_request_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[PullRequestStatus] = mapped_column(
        pgEnum(
            PullRequestStatus,
            name="pull_request_status_enum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
    )
