"""Pydantic schemas for Standup operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StandupBase(BaseModel):
    """Base standup schema."""

    user_id: str = Field(..., min_length=1, max_length=100)
    user_name: str = Field(..., min_length=1, max_length=255)
    yesterday: str = Field(..., min_length=1)
    today: str = Field(..., min_length=1)
    blockers: Optional[str] = None
    sprint_id: Optional[int] = None


class StandupCreate(StandupBase):
    """Schema for creating a standup update."""

    pass


class StandupResponse(StandupBase):
    """Schema for standup responses."""

    id: int
    date: datetime
    has_blockers: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
