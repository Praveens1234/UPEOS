# Date & time normalization

from datetime import datetime
from ..core.constants import DATE_FORMAT

def normalize_date(date_str):
    """
    Normalizes a date string to the standard format.
    
    Args:
        date_str (str): Date string in various formats
        
    Returns:
        str: Normalized date string in DD/MM/YYYY format
    """
    # Try to parse the date string
    try:
        # Handle various common date formats
        for fmt in [DATE_FORMAT, '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                return date_obj.strftime(DATE_FORMAT)
            except ValueError:
                continue
        
        # If none of the formats worked, raise an exception
        raise ValueError(f"Unable to parse date: {date_str}")
    except Exception as e:
        print(f"Warning: Date normalization failed for '{date_str}': {e}")
        return None

def validate_date_format(date_str):
    """
    Validates if a date string is in the correct format.
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False