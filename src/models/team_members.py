from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class TeamMembers(Base):
    __tablename__ = "team_members"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
