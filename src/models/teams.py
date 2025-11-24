from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import Base


class Teams(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
