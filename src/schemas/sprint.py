"""Pydantic schemas for Sprint operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SprintBase(BaseModel):
    """Base sprint schema."""

    name: str = Field(..., min_length=1, max_length=255)
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime
    team_capacity: Optional[int] = Field(None, ge=0)
    committed_points: Optional[int] = Field(None, ge=0)


class SprintCreate(SprintBase):
    """Schema for creating a new sprint."""

    pass


class SprintUpdate(BaseModel):
    """Schema for updating an existing sprint."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    goal: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(planned|active|completed)$")
    team_capacity: Optional[int] = Field(None, ge=0)
    committed_points: Optional[int] = Field(None, ge=0)
    completed_points: Optional[int] = Field(None, ge=0)


class SprintResponse(SprintBase):
    """Schema for sprint responses."""

    id: int
    status: str
    completed_points: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
