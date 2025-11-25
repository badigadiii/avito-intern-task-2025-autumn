import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.db.base import Base


class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class TeamMembers(Base):
    __tablename__ = "team_members"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True
    )
