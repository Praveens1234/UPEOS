# Summary repository

from ..connection import DatabaseConnection
from datetime import datetime

class SummaryRepository:
    """
    Repository for managing date-wise summary data in the database.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def create_or_update_summary(self, centre_id, date, farmer_count, quantity, amount, details_url=None, data_state='OPEN', html_hash=None):
        """
        Creates a new date-wise summary or updates an existing one.
        """
        query = """
        INSERT INTO datewise_summaries 
        (centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash, last_synced)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(centre_id, date) DO UPDATE SET
        farmer_count = excluded.farmer_count,
        quantity = excluded.quantity,
        amount = excluded.amount,
        details_url = excluded.details_url,
        data_state = excluded.data_state,
        html_hash = excluded.html_hash,
        last_synced = CURRENT_TIMESTAMP
        """
        self.db_conn.execute_update(query, (
            centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash
        ))
    
    def get_summary_by_centre_and_date(self, centre_id, date):
        """
        Retrieves a date-wise summary by centre ID and date.
        """
        result = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash
               FROM datewise_summaries 
               WHERE centre_id = ? AND date = ?""", 
            (centre_id, date)
        )
        if result:
            return {
                'id': result[0][0],
                'centre_id': result[0][1],
                'date': result[0][2],
                'farmer_count': result[0][3],
                'quantity': result[0][4],
                'amount': result[0][5],
                'details_url': result[0][6],
                'data_state': result[0][7],
                'html_hash': result[0][8]
            }
        return None
    
    def get_summaries_by_centre(self, centre_id):
        """
        Retrieves all date-wise summaries for a centre.
        """
        results = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash
               FROM datewise_summaries 
               WHERE centre_id = ? 
               ORDER BY date""",
            (centre_id,)
        )
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_count': row[3],
                'quantity': row[4],
                'amount': row[5],
                'details_url': row[6],
                'data_state': row[7],
                'html_hash': row[8]
            }
            for row in results
        ]
    
    def get_latest_summary_for_centre(self, centre_id):
        """
        Retrieves the latest date-wise summary for a centre.
        """
        result = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash
               FROM datewise_summaries 
               WHERE centre_id = ? 
               ORDER BY date DESC 
               LIMIT 1""",
            (centre_id,)
        )
        if result:
            return {
                'id': result[0][0],
                'centre_id': result[0][1],
                'date': result[0][2],
                'farmer_count': result[0][3],
                'quantity': result[0][4],
                'amount': result[0][5],
                'details_url': result[0][6],
                'data_state': result[0][7],
                'html_hash': result[0][8]
            }
        return None
    
    def get_summaries_in_date_range(self, centre_id, from_date, to_date):
        """
        Retrieves date-wise summaries for a centre within a date range.
        """
        results = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_count, quantity, amount, details_url, data_state, html_hash
               FROM datewise_summaries 
               WHERE centre_id = ? AND date BETWEEN ? AND ?
               ORDER BY date""",
            (centre_id, from_date, to_date)
        )
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_count': row[3],
                'quantity': row[4],
                'amount': row[5],
                'details_url': row[6],
                'data_state': row[7],
                'html_hash': row[8]
            }
            for row in results
        ]