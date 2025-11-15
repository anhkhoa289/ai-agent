"""Standup management endpoints."""

from typing import List
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.models.standup import Standup
from src.schemas.standup import StandupCreate, StandupResponse

router = APIRouter()


@router.post("/", response_model=StandupResponse, status_code=status.HTTP_201_CREATED)
async def create_standup(standup: StandupCreate, db: Session = Depends(get_db)):
    """
    Create a new standup update.

    Args:
        standup: Standup creation data
        db: Database session

    Returns:
        StandupResponse: Created standup
    """
    # Check if blockers exist
    has_blockers = bool(standup.blockers and standup.blockers.strip())

    db_standup = Standup(
        **standup.model_dump(),
        has_blockers=has_blockers
    )
    db.add(db_standup)
    db.commit()
    db.refresh(db_standup)
    return db_standup


@router.get("/", response_model=List[StandupResponse])
async def list_standups(
    skip: int = 0,
    limit: int = 100,
    user_id: str = None,
    sprint_id: int = None,
    has_blockers: bool = None,
    date_from: date = None,
    date_to: date = None,
    db: Session = Depends(get_db)
):
    """
    List standups with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        user_id: Filter by user ID
        sprint_id: Filter by sprint ID
        has_blockers: Filter by presence of blockers
        date_from: Filter standups from this date
        date_to: Filter standups until this date
        db: Database session

    Returns:
        List[StandupResponse]: List of standups
    """
    query = db.query(Standup)

    if user_id:
        query = query.filter(Standup.user_id == user_id)
    if sprint_id:
        query = query.filter(Standup.sprint_id == sprint_id)
    if has_blockers is not None:
        query = query.filter(Standup.has_blockers == has_blockers)
    if date_from:
        query = query.filter(Standup.date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Standup.date <= datetime.combine(date_to, datetime.max.time()))

    standups = query.order_by(Standup.date.desc()).offset(skip).limit(limit).all()
    return standups


@router.get("/{standup_id}", response_model=StandupResponse)
async def get_standup(standup_id: int, db: Session = Depends(get_db)):
    """
    Get a specific standup by ID.

    Args:
        standup_id: Standup ID
        db: Database session

    Returns:
        StandupResponse: Standup details

    Raises:
        HTTPException: If standup not found
    """
    standup = db.query(Standup).filter(Standup.id == standup_id).first()
    if not standup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Standup with id {standup_id} not found"
        )
    return standup


@router.delete("/{standup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_standup(standup_id: int, db: Session = Depends(get_db)):
    """
    Delete a standup.

    Args:
        standup_id: Standup ID
        db: Database session

    Raises:
        HTTPException: If standup not found
    """
    standup = db.query(Standup).filter(Standup.id == standup_id).first()
    if not standup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Standup with id {standup_id} not found"
        )

    db.delete(standup)
    db.commit()
