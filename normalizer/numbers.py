# Quantity & amount normalization

def normalize_number(number_str):
    """
    Normalizes a number string to a float value.
    
    Args:
        number_str (str): Number string with possible currency symbols, commas, etc.
        
    Returns:
        float: Normalized number value
    """
    if not number_str:
        return 0.0
    
    try:
        # Remove currency symbols, commas, and other non-numeric characters
        normalized = ''.join(c for c in number_str if c.isdigit() or c in '.-')
        
        # Handle edge cases
        if not normalized:
            return 0.0
        
        # Convert to float
        return float(normalized)
    except Exception as e:
        print(f"Warning: Number normalization failed for '{number_str}': {e}")
        return 0.0

def normalize_integer(int_str):
    """
    Normalizes an integer string to an int value.
    
    Args:
        int_str (str): Integer string
        
    Returns:
        int: Normalized integer value
    """
    if not int_str:
        return 0
    
    try:
        # Remove any non-numeric characters
        normalized = ''.join(c for c in int_str if c.isdigit())
        
        # Handle edge cases
        if not normalized:
            return 0
        
        # Convert to int
        return int(normalized)
    except Exception as e:
        print(f"Warning: Integer normalization failed for '{int_str}': {e}")
        return 0