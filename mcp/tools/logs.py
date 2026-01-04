# Logs MCP tools

from typing import Optional
from ...db.connection import DatabaseConnection
from ...db.repositories.logs_repo import LogsRepository

def get_activity_logs(
    component: Optional[str] = None,
    level: Optional[str] = None,
    limit: int = 100
):
    """
    Retrieves activity logs with optional filtering.
    
    Args:
        component (str, optional): Component to filter by
        level (str, optional): Log level to filter by (INFO, WARNING, ERROR)
        limit (int): Maximum number of logs to return
        
    Returns:
        dict: Dictionary containing logs
    """
    db = DatabaseConnection()
    try:
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
    finally:
        db.close()

def get_recent_errors(limit: int = 10):
    """
    Retrieves recent error logs.
    
    Args:
        limit (int): Maximum number of error logs to return
        
    Returns:
        dict: Dictionary containing error logs
    """
    db = DatabaseConnection()
    try:
        logs_repo = LogsRepository(db)
        errors = logs_repo.get_recent_errors(limit)
        return {"errors": errors}
    finally:
        db.close()