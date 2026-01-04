# Time helpers

from datetime import datetime, timedelta
from ..core.constants import DATE_FORMAT

def get_current_timestamp():
    """
    Gets the current timestamp in ISO format.
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().isoformat()

def parse_date(date_str):
    """
    Parses a date string in DD/MM/YYYY format to a datetime object.
    
    Args:
        date_str (str): Date string in DD/MM/YYYY format
        
    Returns:
        datetime: Parsed datetime object or None if invalid
    """
    try:
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        return None

def format_date(date_obj):
    """
    Formats a datetime object to DD/MM/YYYY string format.
    
    Args:
        date_obj (datetime): Datetime object to format
        
    Returns:
        str: Formatted date string in DD/MM/YYYY format
    """
    if not date_obj:
        return None
    return date_obj.strftime(DATE_FORMAT)

def get_date_range(start_date, end_date):
    """
    Gets a list of dates between start_date and end_date (inclusive).
    
    Args:
        start_date (str): Start date in DD/MM/YYYY format
        end_date (str): End date in DD/MM/YYYY format
        
    Returns:
        list: List of dates in DD/MM/YYYY format
    """
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    if not start or not end:
        return []
    
    dates = []
    current = start
    
    while current <= end:
        dates.append(format_date(current))
        current += timedelta(days=1)
    
    return dates

def is_date_before(date1, date2):
    """
    Checks if date1 is before date2.
    
    Args:
        date1 (str): First date in DD/MM/YYYY format
        date2 (str): Second date in DD/MM/YYYY format
        
    Returns:
        bool: True if date1 is before date2, False otherwise
    """
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    
    if not d1 or not d2:
        return False
    
    return d1 < d2

def is_date_after(date1, date2):
    """
    Checks if date1 is after date2.
    
    Args:
        date1 (str): First date in DD/MM/YYYY format
        date2 (str): Second date in DD/MM/YYYY format
        
    Returns:
        bool: True if date1 is after date2, False otherwise
    """
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    
    if not d1 or not d2:
        return False
    
    return d1 > d2

def get_days_difference(date1, date2):
    """
    Gets the number of days between two dates.
    
    Args:
        date1 (str): First date in DD/MM/YYYY format
        date2 (str): Second date in DD/MM/YYYY format
        
    Returns:
        int: Number of days between the dates (positive if date1 is after date2)
    """
    d1 = parse_date(date1)
    d2 = parse_date(date2)
    
    if not d1 or not d2:
        return 0
    
    return (d1 - d2).days