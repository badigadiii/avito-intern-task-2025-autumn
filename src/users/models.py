import uuid

from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from src.db.base import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        String,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
