# Required-field validation

def validate_required_fields(data, required_fields):
    """
    Validates that all required fields are present and non-empty in the data.
    
    Args:
        data (dict): Data dictionary to validate
        required_fields (list): List of required field names
        
    Returns:
        bool: True if all required fields are present and valid, False otherwise
    """
    for field in required_fields:
        if field not in data or not data[field]:
            print(f"Validation error: Required field '{field}' is missing or empty")
            return False
    return True

def validate_centre_data(centre_data):
    """
    Validates centre data.
    
    Args:
        centre_data (dict): Centre data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['name', 'url']
    return validate_required_fields(centre_data, required_fields)

def validate_datewise_data(datewise_data):
    """
    Validates date-wise summary data.
    
    Args:
        datewise_data (dict): Date-wise summary data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Validate centre name
    if not datewise_data.get('centre_name'):
        print("Validation error: Centre name is missing")
        return False
    
    # Validate dates array
    if 'dates' not in datewise_data or not isinstance(datewise_data['dates'], list):
        print("Validation error: Dates array is missing or invalid")
        return False
    
    # Validate each date entry
    for date_entry in datewise_data['dates']:
        required_fields = ['date', 'farmer_count', 'quantity', 'amount']
        if not validate_required_fields(date_entry, required_fields):
            return False
    
    return True

def validate_farmer_data(farmer_data):
    """
    Validates farmer transaction data.
    
    Args:
        farmer_data (dict): Farmer transaction data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Validate date
    if not farmer_data.get('date'):
        print("Validation error: Date is missing")
        return False
    
    # Validate transactions array
    if 'transactions' not in farmer_data or not isinstance(farmer_data['transactions'], list):
        print("Validation error: Transactions array is missing or invalid")
        return False
    
    # Validate each transaction
    for transaction in farmer_data['transactions']:
        required_fields = ['farmer_id', 'farmer_name', 'village', 'quantity', 'amount']
        if not validate_required_fields(transaction, required_fields):
            return False
    
    return True