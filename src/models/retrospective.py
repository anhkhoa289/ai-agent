"""Retrospective model for database."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Retrospective(Base, TimestampMixin):
    """Retrospective model for sprint retrospectives."""

    __tablename__ = "retrospectives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sprint_id: Mapped[int] = mapped_column(Integer, nullable=False)
    conducted_by: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Retrospective content
    went_well: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    went_wrong: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    improvements: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    action_items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    ai_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Retrospective(id={self.id}, sprint_id={self.sprint_id}, date='{self.date}')>"
