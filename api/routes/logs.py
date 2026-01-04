# Logs API routes

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from ...db.connection import DatabaseConnection
from ...db.repositories.logs_repo import LogsRepository

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

@router.get("/logs")
async def get_activity_logs(
    component: Optional[str] = Query(None, description="Component to filter by"),
    level: Optional[str] = Query(None, description="Log level to filter by (INFO, WARNING, ERROR)"),
    limit: int = Query(100, description="Maximum number of logs to return"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Retrieves activity logs with optional filtering.
    """
    logs_repo = LogsRepository(db)
    
    if component:
        logs = logs_repo.get_logs_by_component(component, limit)
    elif level:
        logs = logs_repo.get_logs_by_level(level, limit)
    else:
        # Get recent logs if no specific filter is provided
        logs = logs_repo.get_logs_by_level('INFO', limit)
        logs.extend(logs_repo.get_logs_by_level('WARNING', limit))
        logs.extend(logs_repo.get_logs_by_level('ERROR', limit))
        # Sort by timestamp descending and limit
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        logs = logs[:limit]
    
    return {"logs": logs}

@router.get("/logs/errors")
async def get_recent_errors(
    limit: int = Query(10, description="Maximum number of error logs to return"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Retrieves recent error logs.
    """
    logs_repo = LogsRepository(db)
    errors = logs_repo.get_recent_errors(limit)
    return {"errors": errors}