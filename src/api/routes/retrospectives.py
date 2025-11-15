"""Retrospective management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.models.retrospective import Retrospective
from src.schemas.retrospective import RetrospectiveCreate, RetrospectiveResponse
from src.agent.scrum_master import get_ai_insights

router = APIRouter()


@router.post("/", response_model=RetrospectiveResponse, status_code=status.HTTP_201_CREATED)
async def create_retrospective(
    retrospective: RetrospectiveCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new retrospective with AI insights.

    Args:
        retrospective: Retrospective creation data
        db: Database session

    Returns:
        RetrospectiveResponse: Created retrospective with AI insights
    """
    # Generate AI insights
    insights = await get_ai_insights(retrospective.model_dump())

    db_retro = Retrospective(
        **retrospective.model_dump(),
        ai_insights=insights
    )
    db.add(db_retro)
    db.commit()
    db.refresh(db_retro)
    return db_retro


@router.get("/", response_model=List[RetrospectiveResponse])
async def list_retrospectives(
    skip: int = 0,
    limit: int = 100,
    sprint_id: int = None,
    db: Session = Depends(get_db)
):
    """
    List retrospectives with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        sprint_id: Filter by sprint ID
        db: Database session

    Returns:
        List[RetrospectiveResponse]: List of retrospectives
    """
    query = db.query(Retrospective)

    if sprint_id:
        query = query.filter(Retrospective.sprint_id == sprint_id)

    retros = query.order_by(Retrospective.date.desc()).offset(skip).limit(limit).all()
    return retros


@router.get("/{retrospective_id}", response_model=RetrospectiveResponse)
async def get_retrospective(retrospective_id: int, db: Session = Depends(get_db)):
    """
    Get a specific retrospective by ID.

    Args:
        retrospective_id: Retrospective ID
        db: Database session

    Returns:
        RetrospectiveResponse: Retrospective details

    Raises:
        HTTPException: If retrospective not found
    """
    retro = db.query(Retrospective).filter(Retrospective.id == retrospective_id).first()
    if not retro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Retrospective with id {retrospective_id} not found"
        )
    return retro


@router.delete("/{retrospective_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_retrospective(retrospective_id: int, db: Session = Depends(get_db)):
    """
    Delete a retrospective.

    Args:
        retrospective_id: Retrospective ID
        db: Database session

    Raises:
        HTTPException: If retrospective not found
    """
    retro = db.query(Retrospective).filter(Retrospective.id == retrospective_id).first()
    if not retro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Retrospective with id {retrospective_id} not found"
        )

    db.delete(retro)
    db.commit()
