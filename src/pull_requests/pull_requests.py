import uuid
from enum import Enum

from sqlalchemy import ForeignKey, String, UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import ENUM as pgEnum

from src.db.base import Base


class PullRequestStatus(Enum):
    OPEN = "open"
    MERGED = "merged"


class PullRequests(Base):
    __tablename__ = "pull_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    pull_request_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[PullRequestStatus] = mapped_column(
        pgEnum(
            PullRequestStatus,
            name="pull_request_status_enum",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
    )
