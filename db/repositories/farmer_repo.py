# Farmer repository

from ..connection import DatabaseConnection

class FarmerRepository:
    """
    Repository for managing farmer transaction data in the database.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def create_or_update_transaction(self, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time=None):
        """
        Creates a new farmer transaction or updates an existing one.
        """
        # Check if this exact transaction already exists to avoid duplicates
        query = """
        SELECT id FROM farmer_transactions 
        WHERE centre_id = ? AND date = ? AND farmer_id = ? AND farmer_name = ? 
        AND village = ? AND quantity = ? AND amount = ? AND transaction_time = ?
        """
        params = (centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time)
        existing = self.db_conn.execute_query(query, params)
        
        if existing:
            # Transaction already exists, update the last_synced timestamp
            update_query = """
            UPDATE farmer_transactions 
            SET last_synced = CURRENT_TIMESTAMP 
            WHERE id = ?
            """
            self.db_conn.execute_update(update_query, (existing[0][0],))
        else:
            # Insert new transaction
            insert_query = """
            INSERT INTO farmer_transactions 
            (centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time, last_synced)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """
            self.db_conn.execute_update(insert_query, (
                centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time
            ))
    
    def get_transactions_by_centre_and_date(self, centre_id, date):
        """
        Retrieves all farmer transactions for a centre on a specific date.
        """
        results = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time
               FROM farmer_transactions 
               WHERE centre_id = ? AND date = ?
               ORDER BY farmer_name""",
            (centre_id, date)
        )
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_id': row[3],
                'farmer_name': row[4],
                'village': row[5],
                'quantity': row[6],
                'amount': row[7],
                'transaction_time': row[8]
            }
            for row in results
        ]
    
    def search_farmer_transactions(self, farmer_name_pattern):
        """
        Searches for farmer transactions by farmer name pattern.
        """
        results = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time
               FROM farmer_transactions 
               WHERE farmer_name LIKE ?
               ORDER BY date DESC, farmer_name""",
            (f'%{farmer_name_pattern}%',)
        )
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_id': row[3],
                'farmer_name': row[4],
                'village': row[5],
                'quantity': row[6],
                'amount': row[7],
                'transaction_time': row[8]
            }
            for row in results
        ]
    
    def get_transactions_by_village(self, village_pattern):
        """
        Retrieves farmer transactions by village pattern.
        """
        results = self.db_conn.execute_query(
            """SELECT id, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time
               FROM farmer_transactions 
               WHERE village LIKE ?
               ORDER BY date DESC, village, farmer_name""",
            (f'%{village_pattern}%',)
        )
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_id': row[3],
                'farmer_name': row[4],
                'village': row[5],
                'quantity': row[6],
                'amount': row[7],
                'transaction_time': row[8]
            }
            for row in results
        ]
    
    def delete_transactions_by_centre_and_date(self, centre_id, date):
        """
        Deletes all farmer transactions for a centre on a specific date.
        This is used when resyncing data to avoid duplicates.
        """
        query = """
        DELETE FROM farmer_transactions 
        WHERE centre_id = ? AND date = ?
        """
        return self.db_conn.execute_update(query, (centre_id, date))