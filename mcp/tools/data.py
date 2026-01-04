# Data MCP tools

from ...db.connection import DatabaseConnection
from ...db.repositories.centre_repo import CentreRepository
from ...db.repositories.summary_repo import SummaryRepository

def get_centre_summary(centre_name: str):
    """
    Gets the summary data for a specific centre.
    
    Args:
        centre_name (str): Name of the centre
        
    Returns:
        dict: Dictionary containing centre and summary data
    """
    db = DatabaseConnection()
    try:
        centre_repo = CentreRepository(db)
        centre = centre_repo.get_centre_by_name(centre_name)
        
        if not centre:
            return {"error": "Centre not found"}
        
        summary_repo = SummaryRepository(db)
        summaries = summary_repo.get_summaries_by_centre(centre['id'])
        
        return {
            "centre": centre,
            "summaries": summaries
        }
    finally:
        db.close()

def get_latest_summary(centre_name: str):
    """
    Gets the latest summary data for a specific centre.
    
    Args:
        centre_name (str): Name of the centre
        
    Returns:
        dict: Dictionary containing centre and latest summary data
    """
    db = DatabaseConnection()
    try:
        centre_repo = CentreRepository(db)
        centre = centre_repo.get_centre_by_name(centre_name)
        
        if not centre:
            return {"error": "Centre not found"}
        
        summary_repo = SummaryRepository(db)
        latest_summary = summary_repo.get_latest_summary_for_centre(centre['id'])
        
        if not latest_summary:
            return {"error": "No summary data found for this centre"}
        
        return {
            "centre": centre,
            "latest_summary": latest_summary
        }
    finally:
        db.close()

def get_date_summary(centre_name: str, date: str):
    """
    Gets the summary data for a specific centre on a specific date.
    
    Args:
        centre_name (str): Name of the centre
        date (str): Date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing centre and summary data for the date
    """
    db = DatabaseConnection()
    try:
        centre_repo = CentreRepository(db)
        centre = centre_repo.get_centre_by_name(centre_name)
        
        if not centre:
            return {"error": "Centre not found"}
        
        summary_repo = SummaryRepository(db)
        summary = summary_repo.get_summary_by_centre_and_date(centre['id'], date)
        
        if not summary:
            return {"error": "No summary data found for this centre on the specified date"}
        
        return {
            "centre": centre,
            "summary": summary
        }
    finally:
        db.close()