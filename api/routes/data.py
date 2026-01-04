# Data API routes

from fastapi import APIRouter, Depends, HTTPException
from ...db.connection import DatabaseConnection
from ...db.repositories.centre_repo import CentreRepository
from ...db.repositories.summary_repo import SummaryRepository

router = APIRouter()

def get_db():
    """
    Dependency to get database connection.
    """
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()

@router.get("/centres/{centre_name}/summary")
async def get_centre_summary(centre_name: str, db: DatabaseConnection = Depends(get_db)):
    """
    Gets the summary data for a specific centre.
    """
    centre_repo = CentreRepository(db)
    centre = centre_repo.get_centre_by_name(centre_name)
    
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    summary_repo = SummaryRepository(db)
    summaries = summary_repo.get_summaries_by_centre(centre['id'])
    
    return {
        "centre": centre,
        "summaries": summaries
    }

@router.get("/centres/{centre_name}/summary/latest")
async def get_latest_summary(centre_name: str, db: DatabaseConnection = Depends(get_db)):
    """
    Gets the latest summary data for a specific centre.
    """
    centre_repo = CentreRepository(db)
    centre = centre_repo.get_centre_by_name(centre_name)
    
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    summary_repo = SummaryRepository(db)
    latest_summary = summary_repo.get_latest_summary_for_centre(centre['id'])
    
    if not latest_summary:
        raise HTTPException(status_code=404, detail="No summary data found for this centre")
    
    return {
        "centre": centre,
        "latest_summary": latest_summary
    }

@router.get("/centres/{centre_name}/summary/{date}")
async def get_date_summary(centre_name: str, date: str, db: DatabaseConnection = Depends(get_db)):
    """
    Gets the summary data for a specific centre on a specific date.
    """
    centre_repo = CentreRepository(db)
    centre = centre_repo.get_centre_by_name(centre_name)
    
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    summary_repo = SummaryRepository(db)
    summary = summary_repo.get_summary_by_centre_and_date(centre['id'], date)
    
    if not summary:
        raise HTTPException(status_code=404, detail="No summary data found for this centre on the specified date")
    
    return {
        "centre": centre,
        "summary": summary
    }