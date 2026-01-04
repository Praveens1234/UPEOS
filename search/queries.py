# SQL query builder

class SQLQueryBuilder:
    """
    Builds SQL queries for searching and filtering data.
    """
    
    def __init__(self):
        pass
    
    def build_farmer_search_query(self, filters):
        """
        Builds a SQL query for searching farmer transactions based on filters.
        
        Args:
            filters (dict): Parsed search filters
            
        Returns:
            tuple: (query_string, parameters)
        """
        # Base query
        query = """
        SELECT ft.id, ft.centre_id, c.name as centre_name, ft.date, ft.farmer_id, 
               ft.farmer_name, ft.village, ft.quantity, ft.amount, ft.transaction_time
        FROM farmer_transactions ft
        JOIN centres c ON ft.centre_id = c.id
        WHERE 1=1
        """
        
        params = []
        
        # Add farmer name filter
        if 'farmer_name' in filters:
            query += " AND ft.farmer_name LIKE ?"
            params.append(f"%{filters['farmer_name']}%")
        
        # Add village filter
        if 'village' in filters:
            query += " AND ft.village LIKE ?"
            params.append(f"%{filters['village']}%")
        
        # Add quantity filters
        if 'min_quantity' in filters:
            query += " AND ft.quantity >= ?"
            params.append(filters['min_quantity'])
        
        # Add quantity filters
        if 'max_quantity' in filters:
            query += " AND ft.quantity <= ?"
            params.append(filters['max_quantity'])
        
        # Add amount filters
        if 'min_amount' in filters:
            query += " AND ft.amount >= ?"
            params.append(filters['min_amount'])
        
        # Add amount filters
        if 'max_amount' in filters:
            query += " AND ft.amount <= ?"
            params.append(filters['max_amount'])
        
        # Add date filters
        if 'from_date' in filters:
            query += " AND ft.date >= ?"
            params.append(filters['from_date'])
        
        if 'to_date' in filters:
            query += " AND ft.date <= ?"
            params.append(filters['to_date'])
        
        # Order by date descending and farmer name
        query += " ORDER BY ft.date DESC, ft.farmer_name"
        
        return query, params
    
    def build_village_search_query(self, filters):
        """
        Builds a SQL query for searching by village with filters.
        
        Args:
            filters (dict): Parsed search filters
            
        Returns:
            tuple: (query_string, parameters)
        """
        # Base query
        query = """
        SELECT DISTINCT ft.village
        FROM farmer_transactions ft
        WHERE ft.village LIKE ?
        """
        
        params = [f"%{filters.get('village', '')}%"]
        
        # Add date filters
        if 'from_date' in filters:
            query += " AND ft.date >= ?"
            params.append(filters['from_date'])
        
        if 'to_date' in filters:
            query += " AND ft.date <= ?"
            params.append(filters['to_date'])
        
        # Order by village name
        query += " ORDER BY ft.village"
        
        return query, params
    
    def build_advanced_search_query(self, filters):
        """
        Builds a SQL query for advanced search with multiple criteria.
        
        Args:
            filters (dict): Parsed search filters
            
        Returns:
            tuple: (query_string, parameters)
        """
        # Base query
        query = """
        SELECT ft.id, ft.centre_id, c.name as centre_name, ft.date, ft.farmer_id, 
               ft.farmer_name, ft.village, ft.quantity, ft.amount, ft.transaction_time
        FROM farmer_transactions ft
        JOIN centres c ON ft.centre_id = c.id
        WHERE 1=1
        """
        
        params = []
        
        # Add all applicable filters
        # Farmer name filter
        if 'farmer_name' in filters:
            query += " AND ft.farmer_name LIKE ?"
            params.append(f"%{filters['farmer_name']}%")
        
        # Village filter
        if 'village' in filters:
            query += " AND ft.village LIKE ?"
            params.append(f"%{filters['village']}%")
        
        # Quantity filters
        if 'min_quantity' in filters:
            query += " AND ft.quantity >= ?"
            params.append(filters['min_quantity'])
        
        if 'max_quantity' in filters:
            query += " AND ft.quantity <= ?"
            params.append(filters['max_quantity'])
        
        # Amount filters
        if 'min_amount' in filters:
            query += " AND ft.amount >= ?"
            params.append(filters['min_amount'])
        
        if 'max_amount' in filters:
            query += " AND ft.amount <= ?"
            params.append(filters['max_amount'])
        
        # Date filters
        if 'from_date' in filters:
            query += " AND ft.date >= ?"
            params.append(filters['from_date'])
        
        if 'to_date' in filters:
            query += " AND ft.date <= ?"
            params.append(filters['to_date'])
        
        # Order by date descending and farmer name
        query += " ORDER BY ft.date DESC, ft.farmer_name"
        
        return query, params