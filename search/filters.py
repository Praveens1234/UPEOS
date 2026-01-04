# Filter parsing & validation

class SearchFilters:
    """
    Manages parsing and validation of search filters.
    """
    
    def __init__(self, filters_dict=None):
        self.filters = filters_dict or {}
        self.parsed_filters = {}
        self.errors = []
        self._parse_filters()
    
    def _parse_filters(self):
        """
        Parses and validates filter parameters.
        """
        # Parse farmer name filter
        if 'farmer_name' in self.filters:
            farmer_name = self.filters['farmer_name']
            if isinstance(farmer_name, str) and len(farmer_name.strip()) > 0:
                self.parsed_filters['farmer_name'] = farmer_name.strip()
            else:
                self.errors.append("Invalid farmer_name filter: must be a non-empty string")
        
        # Parse village filter
        if 'village' in self.filters:
            village = self.filters['village']
            if isinstance(village, str) and len(village.strip()) > 0:
                self.parsed_filters['village'] = village.strip()
            else:
                self.errors.append("Invalid village filter: must be a non-empty string")
        
        # Parse quantity range filters
        if 'min_quantity' in self.filters:
            try:
                min_quantity = float(self.filters['min_quantity'])
                self.parsed_filters['min_quantity'] = min_quantity
            except (ValueError, TypeError):
                self.errors.append("Invalid min_quantity filter: must be a number")
        
        if 'max_quantity' in self.filters:
            try:
                max_quantity = float(self.filters['max_quantity'])
                self.parsed_filters['max_quantity'] = max_quantity
            except (ValueError, TypeError):
                self.errors.append("Invalid max_quantity filter: must be a number")
        
        # Validate quantity range
        if 'min_quantity' in self.parsed_filters and 'max_quantity' in self.parsed_filters:
            if self.parsed_filters['min_quantity'] > self.parsed_filters['max_quantity']:
                self.errors.append("Invalid quantity range: min_quantity cannot be greater than max_quantity")
        
        # Parse amount range filters
        if 'min_amount' in self.filters:
            try:
                min_amount = float(self.filters['min_amount'])
                self.parsed_filters['min_amount'] = min_amount
            except (ValueError, TypeError):
                self.errors.append("Invalid min_amount filter: must be a number")
        
        if 'max_amount' in self.filters:
            try:
                max_amount = float(self.filters['max_amount'])
                self.parsed_filters['max_amount'] = max_amount
            except (ValueError, TypeError):
                self.errors.append("Invalid max_amount filter: must be a number")
        
        # Validate amount range
        if 'min_amount' in self.parsed_filters and 'max_amount' in self.parsed_filters:
            if self.parsed_filters['min_amount'] > self.parsed_filters['max_amount']:
                self.errors.append("Invalid amount range: min_amount cannot be greater than max_amount")
        
        # Parse date range filters
        if 'from_date' in self.filters:
            from_date = self.filters['from_date']
            if isinstance(from_date, str) and len(from_date.strip()) > 0:
                # Basic validation - in a real implementation, we would validate the date format
                self.parsed_filters['from_date'] = from_date.strip()
            else:
                self.errors.append("Invalid from_date filter: must be a non-empty string")
        
        if 'to_date' in self.filters:
            to_date = self.filters['to_date']
            if isinstance(to_date, str) and len(to_date.strip()) > 0:
                # Basic validation - in a real implementation, we would validate the date format
                self.parsed_filters['to_date'] = to_date.strip()
            else:
                self.errors.append("Invalid to_date filter: must be a non-empty string")
    
    def get_parsed_filters(self):
        """
        Returns the parsed filters.
        
        Returns:
            dict: Parsed filters
        """
        return self.parsed_filters
    
    def get_errors(self):
        """
        Returns any filter parsing errors.
        
        Returns:
            list: List of error messages
        """
        return self.errors
    
    def is_valid(self):
        """
        Checks if all filters are valid.
        
        Returns:
            bool: True if all filters are valid, False otherwise
        """
        return len(self.errors) == 0