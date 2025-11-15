"""Sprint model for database."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Sprint(Base, TimestampMixin):
    """Sprint model representing an agile sprint cycle."""

    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    goal: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="planned",
        nullable=False
    )  # planned, active, completed
    team_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    committed_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completed_points: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<Sprint(id={self.id}, name='{self.name}', status='{self.status}')>"
