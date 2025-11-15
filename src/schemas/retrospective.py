"""Pydantic schemas for Retrospective operations."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class RetrospectiveBase(BaseModel):
    """Base retrospective schema."""

    sprint_id: int
    conducted_by: str = Field(..., min_length=1, max_length=255)
    went_well: Optional[Dict[str, Any]] = None
    went_wrong: Optional[Dict[str, Any]] = None
    improvements: Optional[Dict[str, Any]] = None
    action_items: Optional[Dict[str, Any]] = None


class RetrospectiveCreate(RetrospectiveBase):
    """Schema for creating a retrospective."""

    pass


class RetrospectiveResponse(RetrospectiveBase):
    """Schema for retrospective responses."""

    id: int
    date: datetime
    ai_insights: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
