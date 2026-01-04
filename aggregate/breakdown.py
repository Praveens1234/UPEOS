# Date-wise & centre-wise breakdowns

from ..db.connection import DatabaseConnection

class BreakdownAggregator:
    """
    Aggregates date-wise and centre-wise breakdowns of procurement data.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def get_daily_breakdown(self, centre_id=None, from_date=None, to_date=None):
        """
        Gets a date-wise breakdown of procurement data.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            list: List of daily breakdown entries
        """
        query = """
        SELECT 
            date,
            SUM(farmer_count) as total_farmers,
            SUM(quantity) as total_quantity,
            SUM(amount) as total_amount,
            COUNT(DISTINCT centre_id) as centre_count
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
        
        query += " GROUP BY date ORDER BY date"
        
        results = self.db_conn.execute_query(query, params)
        
        return [
            {
                'date': row[0],
                'total_farmers': row[1] or 0,
                'total_quantity': row[2] or 0,
                'total_amount': row[3] or 0,
                'centre_count': row[4] or 0
            }
            for row in results
        ]
    
    def get_centre_comparison(self, date=None, from_date=None, to_date=None):
        """
        Gets a centre-wise comparison of procurement data.
        
        Args:
            date (str, optional): Specific date in DD/MM/YYYY format
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            list: List of centre comparison entries
        """
        query = """
        SELECT 
            c.id as centre_id,
            c.name as centre_name,
            SUM(dws.farmer_count) as total_farmers,
            SUM(dws.quantity) as total_quantity,
            SUM(dws.amount) as total_amount,
            COUNT(dws.date) as active_days
        FROM datewise_summaries dws
        JOIN centres c ON dws.centre_id = c.id
        WHERE 1=1
        """
        params = []
        
        if date:
            query += " AND dws.date = ?"
            params.append(date)
        
        if from_date:
            query += " AND dws.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND dws.date <= ?"
            params.append(to_date)
        
        query += " GROUP BY c.id, c.name ORDER BY total_quantity DESC"
        
        results = self.db_conn.execute_query(query, params)
        
        return [
            {
                'centre_id': row[0],
                'centre_name': row[1],
                'total_farmers': row[2] or 0,
                'total_quantity': row[3] or 0,
                'total_amount': row[4] or 0,
                'active_days': row[5] or 0
            }
            for row in results
        ]
    
    def get_top_centres_by_quantity(self, limit=10, from_date=None, to_date=None):
        """
        Gets the top centres by total quantity procured.
        
        Args:
            limit (int): Maximum number of centres to return
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            list: List of top centres by quantity
        """
        query = """
        SELECT 
            c.id as centre_id,
            c.name as centre_name,
            SUM(dws.quantity) as total_quantity,
            SUM(dws.amount) as total_amount,
            SUM(dws.farmer_count) as total_farmers
        FROM datewise_summaries dws
        JOIN centres c ON dws.centre_id = c.id
        WHERE 1=1
        """
        params = []
        
        if from_date:
            query += " AND dws.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND dws.date <= ?"
            params.append(to_date)
        
        query += " GROUP BY c.id, c.name ORDER BY total_quantity DESC LIMIT ?"
        params.append(limit)
        
        results = self.db_conn.execute_query(query, params)
        
        return [
            {
                'centre_id': row[0],
                'centre_name': row[1],
                'total_quantity': row[2] or 0,
                'total_amount': row[3] or 0,
                'total_farmers': row[4] or 0
            }
            for row in results
        ]
    
    def get_top_centres_by_amount(self, limit=10, from_date=None, to_date=None):
        """
        Gets the top centres by total amount paid.
        
        Args:
            limit (int): Maximum number of centres to return
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            list: List of top centres by amount
        """
        query = """
        SELECT 
            c.id as centre_id,
            c.name as centre_name,
            SUM(dws.amount) as total_amount,
            SUM(dws.quantity) as total_quantity,
            SUM(dws.farmer_count) as total_farmers
        FROM datewise_summaries dws
        JOIN centres c ON dws.centre_id = c.id
        WHERE 1=1
        """
        params = []
        
        if from_date:
            query += " AND dws.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND dws.date <= ?"
            params.append(to_date)
        
        query += " GROUP BY c.id, c.name ORDER BY total_amount DESC LIMIT ?"
        params.append(limit)
        
        results = self.db_conn.execute_query(query, params)
        
        return [
            {
                'centre_id': row[0],
                'centre_name': row[1],
                'total_amount': row[2] or 0,
                'total_quantity': row[3] or 0,
                'total_farmers': row[4] or 0
            }
            for row in results
        ]