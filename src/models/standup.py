"""Standup model for database."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class Standup(Base, TimestampMixin):
    """Standup model representing daily standup updates."""

    __tablename__ = "standups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sprint_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    # Standup content
    yesterday: Mapped[str] = mapped_column(Text, nullable=False)
    today: Mapped[str] = mapped_column(Text, nullable=False)
    blockers: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    has_blockers: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Standup(id={self.id}, user='{self.user_name}', date='{self.date}')>"
