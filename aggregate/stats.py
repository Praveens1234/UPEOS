# Quantity/amount/farmer aggregates

from ..db.connection import DatabaseConnection

class StatsAggregator:
    """
    Aggregates statistics for quantity, amount, and farmer counts.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def get_total_quantity(self, centre_id=None, from_date=None, to_date=None):
        """
        Gets the total quantity aggregated by centre and/or date range.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            dict: Total quantity and related information
        """
        query = """
        SELECT SUM(quantity) as total_quantity, COUNT(*) as entry_count
        FROM datewise_summaries
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND centre_id = ?"
            params.append(centre_id)
        
        if from_date:
            query += " AND date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND date <= ?"
            params.append(to_date)
        
        result = self.db_conn.execute_query(query, params)
        
        if result and result[0][0] is not None:
            return {
                'total_quantity': result[0][0],
                'entry_count': result[0][1]
            }
        else:
            return {
                'total_quantity': 0,
                'entry_count': 0
            }
    
    def get_total_amount(self, centre_id=None, from_date=None, to_date=None):
        """
        Gets the total amount aggregated by centre and/or date range.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            dict: Total amount and related information
        """
        query = """
        SELECT SUM(amount) as total_amount, COUNT(*) as entry_count
        FROM datewise_summaries
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND centre_id = ?"
            params.append(centre_id)
        
        if from_date:
            query += " AND date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND date <= ?"
            params.append(to_date)
        
        result = self.db_conn.execute_query(query, params)
        
        if result and result[0][0] is not None:
            return {
                'total_amount': result[0][0],
                'entry_count': result[0][1]
            }
        else:
            return {
                'total_amount': 0,
                'entry_count': 0
            }
    
    def get_total_farmers(self, centre_id=None, from_date=None, to_date=None):
        """
        Gets the total farmer count aggregated by centre and/or date range.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            dict: Total farmer count and related information
        """
        query = """
        SELECT SUM(farmer_count) as total_farmers, COUNT(*) as entry_count
        FROM datewise_summaries
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND centre_id = ?"
            params.append(centre_id)
        
        if from_date:
            query += " AND date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND date <= ?"
            params.append(to_date)
        
        result = self.db_conn.execute_query(query, params)
        
        if result and result[0][0] is not None:
            return {
                'total_farmers': result[0][0],
                'entry_count': result[0][1]
            }
        else:
            return {
                'total_farmers': 0,
                'entry_count': 0
            }
    
    def get_stats(self, centre_id=None, date=None):
        """
        Gets comprehensive statistics for a specific centre and/or date.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            date (str, optional): Date in DD/MM/YYYY format
            
        Returns:
            dict: Statistics including quantity, amount, and farmer count
        """
        query = """
        SELECT 
            SUM(quantity) as total_quantity,
            SUM(amount) as total_amount,
            SUM(farmer_count) as total_farmers,
            COUNT(*) as entry_count
        FROM datewise_summaries
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND centre_id = ?"
            params.append(centre_id)
        
        if date:
            query += " AND date = ?"
            params.append(date)
        
        result = self.db_conn.execute_query(query, params)
        
        if result and result[0][0] is not None:
            return {
                'total_quantity': result[0][0] or 0,
                'total_amount': result[0][1] or 0,
                'total_farmers': result[0][2] or 0,
                'entry_count': result[0][3] or 0
            }
        else:
            return {
                'total_quantity': 0,
                'total_amount': 0,
                'total_farmers': 0,
                'entry_count': 0
            }