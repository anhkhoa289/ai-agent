"""Sprint management endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.storage.database import get_db
from src.models.sprint import Sprint
from src.schemas.sprint import SprintCreate, SprintResponse, SprintUpdate

router = APIRouter()


@router.post("/", response_model=SprintResponse, status_code=status.HTTP_201_CREATED)
async def create_sprint(sprint: SprintCreate, db: Session = Depends(get_db)):
    """
    Create a new sprint.

    Args:
        sprint: Sprint creation data
        db: Database session

    Returns:
        SprintResponse: Created sprint
    """
    db_sprint = Sprint(**sprint.model_dump())
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    return db_sprint


@router.get("/", response_model=List[SprintResponse])
async def list_sprints(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db)
):
    """
    List all sprints with optional filtering.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        status_filter: Filter by sprint status
        db: Database session

    Returns:
        List[SprintResponse]: List of sprints
    """
    query = db.query(Sprint)

    if status_filter:
        query = query.filter(Sprint.status == status_filter)

    sprints = query.offset(skip).limit(limit).all()
    return sprints


@router.get("/{sprint_id}", response_model=SprintResponse)
async def get_sprint(sprint_id: int, db: Session = Depends(get_db)):
    """
    Get a specific sprint by ID.

    Args:
        sprint_id: Sprint ID
        db: Database session

    Returns:
        SprintResponse: Sprint details

    Raises:
        HTTPException: If sprint not found
    """
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sprint with id {sprint_id} not found"
        )
    return sprint


@router.patch("/{sprint_id}", response_model=SprintResponse)
async def update_sprint(
    sprint_id: int,
    sprint_update: SprintUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a sprint.

    Args:
        sprint_id: Sprint ID
        sprint_update: Sprint update data
        db: Database session

    Returns:
        SprintResponse: Updated sprint

    Raises:
        HTTPException: If sprint not found
    """
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sprint with id {sprint_id} not found"
        )

    update_data = sprint_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sprint, field, value)

    db.commit()
    db.refresh(sprint)
    return sprint


@router.delete("/{sprint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sprint(sprint_id: int, db: Session = Depends(get_db)):
    """
    Delete a sprint.

    Args:
        sprint_id: Sprint ID
        db: Database session

    Raises:
        HTTPException: If sprint not found
    """
    sprint = db.query(Sprint).filter(Sprint.id == sprint_id).first()
    if not sprint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sprint with id {sprint_id} not found"
        )

    db.delete(sprint)
    db.commit()
