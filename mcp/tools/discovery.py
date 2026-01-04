# Discovery MCP tools

from ...db.connection import DatabaseConnection
from ...db.repositories.centre_repo import CentreRepository

def list_centres():
    """
    Lists all procurement centres.
    
    Returns:
        dict: Dictionary containing the list of centres
    """
    db = DatabaseConnection()
    try:
        centre_repo = CentreRepository(db)
        centres = centre_repo.get_all_centres()
        return {"centres": centres}
    finally:
        db.close()

def list_centres_by_district(district_name: str):
    """
    Lists all procurement centres in a specific district.
    
    Args:
        district_name (str): Name of the district
        
    Returns:
        dict: Dictionary containing the list of centres in the district
    """
    db = DatabaseConnection()
    try:
        centre_repo = CentreRepository(db)
        centres = centre_repo.get_centres_by_district(district_name)
        return {"centres": centres}
    finally:
        db.close()