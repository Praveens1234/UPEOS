# Search MCP tools

from typing import Optional
from ...db.connection import DatabaseConnection
from ...search.engine import SearchEngine

def search_farmer(
    farmer_name: str,
    village: Optional[str] = None,
    min_quantity: Optional[float] = None,
    max_quantity: Optional[float] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """
    Searches for farmer transactions based on various criteria.
    
    Args:
        farmer_name (str): Farmer name or partial name to search for
        village (str, optional): Village name or partial name to filter by
        min_quantity (float, optional): Minimum quantity filter
        max_quantity (float, optional): Maximum quantity filter
        min_amount (float, optional): Minimum amount filter
        max_amount (float, optional): Maximum amount filter
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing search results
    """
    db = DatabaseConnection()
    try:
        search_engine = SearchEngine(db)
        
        filters = {
            'farmer_name': farmer_name
        }
        
        if village:
            filters['village'] = village
        if min_quantity is not None:
            filters['min_quantity'] = min_quantity
        if max_quantity is not None:
            filters['max_quantity'] = max_quantity
        if min_amount is not None:
            filters['min_amount'] = min_amount
        if max_amount is not None:
            filters['max_amount'] = max_amount
        if from_date:
            filters['from_date'] = from_date
        if to_date:
            filters['to_date'] = to_date
        
        result = search_engine.search_farmers(filters)
        return result
    finally:
        db.close()

def search_by_village(
    village: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """
    Searches for villages matching the given criteria.
    
    Args:
        village (str): Village name or partial name to search for
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing search results
    """
    db = DatabaseConnection()
    try:
        search_engine = SearchEngine(db)
        
        filters = {
            'village': village
        }
        
        if from_date:
            filters['from_date'] = from_date
        if to_date:
            filters['to_date'] = to_date
        
        result = search_engine.search_by_village(filters)
        return result
    finally:
        db.close()

def advanced_search(
    farmer_name: Optional[str] = None,
    village: Optional[str] = None,
    min_quantity: Optional[float] = None,
    max_quantity: Optional[float] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
):
    """
    Performs an advanced search with multiple criteria.
    
    Args:
        farmer_name (str, optional): Farmer name or partial name to search for
        village (str, optional): Village name or partial name to filter by
        min_quantity (float, optional): Minimum quantity filter
        max_quantity (float, optional): Maximum quantity filter
        min_amount (float, optional): Minimum amount filter
        max_amount (float, optional): Maximum amount filter
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing search results
    """
    db = DatabaseConnection()
    try:
        search_engine = SearchEngine(db)
        
        filters = {}
        
        if farmer_name:
            filters['farmer_name'] = farmer_name
        if village:
            filters['village'] = village
        if min_quantity is not None:
            filters['min_quantity'] = min_quantity
        if max_quantity is not None:
            filters['max_quantity'] = max_quantity
        if min_amount is not None:
            filters['min_amount'] = min_amount
        if max_amount is not None:
            filters['max_amount'] = max_amount
        if from_date:
            filters['from_date'] = from_date
        if to_date:
            filters['to_date'] = to_date
        
        result = search_engine.advanced_search(filters)
        return result
    finally:
        db.close()