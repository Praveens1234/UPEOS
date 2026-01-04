# Search execution

from ..db.connection import DatabaseConnection
from .filters import SearchFilters
from .queries import SQLQueryBuilder

class SearchEngine:
    """
    Executes searches against the database using parsed filters.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
        self.query_builder = SQLQueryBuilder()
    
    def search_farmers(self, filters_dict):
        """
        Searches for farmer transactions based on filters.
        
        Args:
            filters_dict (dict): Raw filter parameters
            
        Returns:
            dict: Search results or error information
        """
        # Parse and validate filters
        filters = SearchFilters(filters_dict)
        if not filters.is_valid():
            return {
                'status': 'error',
                'errors': filters.get_errors()
            }
        
        # Build query
        parsed_filters = filters.get_parsed_filters()
        query, params = self.query_builder.build_farmer_search_query(parsed_filters)
        
        # Execute query
        try:
            results = self.db_conn.execute_query(query, params)
            return {
                'status': 'success',
                'data': [
                    {
                        'id': row[0],
                        'centre_id': row[1],
                        'centre_name': row[2],
                        'date': row[3],
                        'farmer_id': row[4],
                        'farmer_name': row[5],
                        'village': row[6],
                        'quantity': row[7],
                        'amount': row[8],
                        'transaction_time': row[9]
                    }
                    for row in results
                ]
            }
        except Exception as e:
            return {
                'status': 'error',
                'errors': [f"Database query failed: {str(e)}"]
            }
    
    def search_by_village(self, filters_dict):
        """
        Searches for villages based on filters.
        
        Args:
            filters_dict (dict): Raw filter parameters
            
        Returns:
            dict: Search results or error information
        """
        # Parse and validate filters
        filters = SearchFilters(filters_dict)
        if not filters.is_valid():
            return {
                'status': 'error',
                'errors': filters.get_errors()
            }
        
        # Build query
        parsed_filters = filters.get_parsed_filters()
        query, params = self.query_builder.build_village_search_query(parsed_filters)
        
        # Execute query
        try:
            results = self.db_conn.execute_query(query, params)
            return {
                'status': 'success',
                'data': [{'village': row[0]} for row in results]
            }
        except Exception as e:
            return {
                'status': 'error',
                'errors': [f"Database query failed: {str(e)}"]
            }
    
    def advanced_search(self, filters_dict):
        """
        Performs an advanced search with multiple criteria.
        
        Args:
            filters_dict (dict): Raw filter parameters
            
        Returns:
            dict: Search results or error information
        """
        # Parse and validate filters
        filters = SearchFilters(filters_dict)
        if not filters.is_valid():
            return {
                'status': 'error',
                'errors': filters.get_errors()
            }
        
        # Build query
        parsed_filters = filters.get_parsed_filters()
        query, params = self.query_builder.build_advanced_search_query(parsed_filters)
        
        # Execute query
        try:
            results = self.db_conn.execute_query(query, params)
            return {
                'status': 'success',
                'data': [
                    {
                        'id': row[0],
                        'centre_id': row[1],
                        'centre_name': row[2],
                        'date': row[3],
                        'farmer_id': row[4],
                        'farmer_name': row[5],
                        'village': row[6],
                        'quantity': row[7],
                        'amount': row[8],
                        'transaction_time': row[9]
                    }
                    for row in results
                ]
            }
        except Exception as e:
            return {
                'status': 'error',
                'errors': [f"Database query failed: {str(e)}"]
            }