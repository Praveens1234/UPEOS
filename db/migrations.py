# Schema/version handling

import sqlite3
import os
from .connection import DatabaseConnection

class DatabaseMigration:
    """
    Handles database schema migrations and versioning.
    """
    
    def __init__(self, db_connection):
        self.db_conn = db_connection
        self.current_version = self._get_current_version()
    
    def _get_current_version(self):
        """
        Gets the current database schema version.
        """
        # For now, we'll use a simple approach of checking if tables exist
        # In a more complex system, we would have a dedicated migrations table
        try:
            result = self.db_conn.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='centres'"
            )
            return 1 if result else 0
        except Exception:
            return 0
    
    def migrate_to_latest(self):
        """
        Migrates the database to the latest schema version.
        """
        # Since we're starting with version 1, we just need to ensure
        # the schema is properly initialized
        if self.current_version < 1:
            self._apply_initial_schema()
            self.current_version = 1
    
    def _apply_initial_schema(self):
        """
        Applies the initial database schema.
        """
        schema_file = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_file):
            with open(schema_file, 'r') as f:
                schema = f.read()
                conn = self.db_conn.get_connection()
                conn.executescript(schema)
        else:
            raise FileNotFoundError(f"Schema file not found: {schema_file}")
    
    def get_version(self):
        """
        Returns the current database version.
        """
        return self.current_version