# SQLite connection & transactions

import sqlite3
import os
from ..config.settings import Settings

class DatabaseConnection:
    """
    Manages SQLite database connections and transactions.
    """
    
    def __init__(self, db_path=None):
        self.settings = Settings()
        self.db_path = db_path or self.settings.database_path or "./data/upeos.db"
        self.connection = None
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self):
        """
        Initializes the database by creating tables if they don't exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
                schema = f.read()
                conn.executescript(schema)
            
            # Check if we need to update the farmer_transactions table
            # This is needed because SQLite doesn't support dropping constraints directly
            cursor = conn.cursor()
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='farmer_transactions'")
            result = cursor.fetchone()
            
            if result and 'UNIQUE(centre_id, date, farmer_id)' in result[0]:
                print("Updating farmer_transactions table to remove UNIQUE constraint...")
                # We need to recreate the table without the UNIQUE constraint
                # First, rename the existing table
                try:
                    cursor.execute("ALTER TABLE farmer_transactions RENAME TO farmer_transactions_old")
                    
                    # Create the new table with the correct schema
                    cursor.execute("""
                    CREATE TABLE farmer_transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        centre_id INTEGER NOT NULL,
                        date DATE NOT NULL,
                        farmer_id TEXT,
                        farmer_name TEXT,
                        village TEXT,
                        quantity REAL,
                        amount REAL,
                        transaction_time TEXT,
                        last_synced TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (centre_id) REFERENCES centres (id)
                    )
                    """)
                    
                    # Copy data from old table to new table
                    cursor.execute("""
                    INSERT INTO farmer_transactions 
                    (id, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time, last_synced)
                    SELECT id, centre_id, date, farmer_id, farmer_name, village, quantity, amount, transaction_time, last_synced
                    FROM farmer_transactions_old
                    """)
                    
                    # Drop the old table
                    cursor.execute("DROP TABLE farmer_transactions_old")
                    
                    # Recreate indexes
                    cursor.execute("CREATE INDEX IF NOT EXISTS idx_farmer_centre_date ON farmer_transactions(centre_id, date)")
                    
                    conn.commit()
                    print("Successfully updated farmer_transactions table")
                except sqlite3.Error as e:
                    print(f"Error updating farmer_transactions table: {e}")
                    # Rollback the changes
                    conn.rollback()
    
    def get_connection(self):
        """
        Gets a database connection.
        """
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            # Enable foreign key constraints
            self.connection.execute("PRAGMA foreign_keys = ON")
        return self.connection
    
    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """
        Executes a SELECT query and returns the results.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    
    def execute_update(self, query, params=None):
        """
        Executes an INSERT/UPDATE/DELETE query.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
    
    def execute_transaction(self, queries_and_params):
        """
        Executes multiple queries in a transaction.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for query, params in queries_and_params:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e