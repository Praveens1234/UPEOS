# Statistics MCP tools

from ...db.connection import DatabaseConnection
from ...aggregate.stats import StatsAggregator

def get_stats(centre_id: int = None, date: str = None):
    """
    Gets comprehensive statistics for a specific centre and/or date.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        date (str, optional): Date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing statistics
    """
    db = DatabaseConnection()
    try:
        aggregator = StatsAggregator(db)
        stats = aggregator.get_stats(centre_id, date)
        return {"stats": stats}
    finally:
        db.close()

def get_total_quantity(centre_id: int = None, from_date: str = None, to_date: str = None):
    """
    Gets the total quantity aggregated by centre and/or date range.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing total quantity
    """
    db = DatabaseConnection()
    try:
        aggregator = StatsAggregator(db)
        total = aggregator.get_total_quantity(centre_id, from_date, to_date)
        return {"total_quantity": total}
    finally:
        db.close()

def get_total_amount(centre_id: int = None, from_date: str = None, to_date: str = None):
    """
    Gets the total amount aggregated by centre and/or date range.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing total amount
    """
    db = DatabaseConnection()
    try:
        aggregator = StatsAggregator(db)
        total = aggregator.get_total_amount(centre_id, from_date, to_date)
        return {"total_amount": total}
    finally:
        db.close()

def get_total_farmers(centre_id: int = None, from_date: str = None, to_date: str = None):
    """
    Gets the total farmer count aggregated by centre and/or date range.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing total farmer count
    """
    db = DatabaseConnection()
    try:
        aggregator = StatsAggregator(db)
        total = aggregator.get_total_farmers(centre_id, from_date, to_date)
        return {"total_farmers": total}
    finally:
        db.close()