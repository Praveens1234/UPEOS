# Logs repository

from ..connection import DatabaseConnection
from datetime import datetime

class LogsRepository:
    """
    Repository for managing activity logs in the database.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def add_log(self, component, level, message, details=None):
        """
        Adds a new activity log entry.
        """
        query = """
        INSERT INTO activity_logs (component, level, message, details)
        VALUES (?, ?, ?, ?)
        """
        self.db_conn.execute_update(query, (component, level, message, details))
    
    def get_logs_by_component(self, component, limit=100):
        """
        Retrieves activity logs by component.
        """
        results = self.db_conn.execute_query(
            """SELECT id, timestamp, component, level, message, details
               FROM activity_logs 
               WHERE component = ?
               ORDER BY timestamp DESC
               LIMIT ?""",
            (component, limit)
        )
        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'component': row[2],
                'level': row[3],
                'message': row[4],
                'details': row[5]
            }
            for row in results
        ]
    
    def get_logs_by_level(self, level, limit=100):
        """
        Retrieves activity logs by level.
        """
        results = self.db_conn.execute_query(
            """SELECT id, timestamp, component, level, message, details
               FROM activity_logs 
               WHERE level = ?
               ORDER BY timestamp DESC
               LIMIT ?""",
            (level, limit)
        )
        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'component': row[2],
                'level': row[3],
                'message': row[4],
                'details': row[5]
            }
            for row in results
        ]
    
    def get_logs_in_time_range(self, from_timestamp, to_timestamp, limit=100):
        """
        Retrieves activity logs within a time range.
        """
        results = self.db_conn.execute_query(
            """SELECT id, timestamp, component, level, message, details
               FROM activity_logs 
               WHERE timestamp BETWEEN ? AND ?
               ORDER BY timestamp DESC
               LIMIT ?""",
            (from_timestamp, to_timestamp, limit)
        )
        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'component': row[2],
                'level': row[3],
                'message': row[4],
                'details': row[5]
            }
            for row in results
        ]
    
    def get_recent_errors(self, limit=10):
        """
        Retrieves recent error logs.
        """
        return self.get_logs_by_level('ERROR', limit)