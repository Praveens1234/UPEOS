# Centre repository

from ..connection import DatabaseConnection

class CentreRepository:
    """
    Repository for managing centre data in the database.
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_conn = db_connection
    
    def create_or_update_centre(self, name, url, district=None):
        """
        Creates a new centre or updates an existing one.
        """
        query = """
        INSERT INTO centres (name, url, district, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(name) DO UPDATE SET
        url = excluded.url,
        district = excluded.district,
        updated_at = CURRENT_TIMESTAMP
        """
        self.db_conn.execute_update(query, (name, url, district))
        
        # Retrieve the centre ID
        result = self.db_conn.execute_query(
            "SELECT id FROM centres WHERE name = ?", (name,)
        )
        return result[0][0] if result else None
    
    def get_centre_by_name(self, name):
        """
        Retrieves a centre by its name.
        """
        result = self.db_conn.execute_query(
            "SELECT id, name, url, district FROM centres WHERE name = ?", (name,)
        )
        if result:
            return {
                'id': result[0][0],
                'name': result[0][1],
                'url': result[0][2],
                'district': result[0][3]
            }
        return None
    
    def get_all_centres(self):
        """
        Retrieves all centres.
        """
        results = self.db_conn.execute_query(
            "SELECT id, name, url, district FROM centres ORDER BY name"
        )
        return [
            {
                'id': row[0],
                'name': row[1],
                'url': row[2],
                'district': row[3]
            }
            for row in results
        ]
    
    def get_centres_by_district(self, district):
        """
        Retrieves centres by district.
        """
        results = self.db_conn.execute_query(
            "SELECT id, name, url, district FROM centres WHERE district = ? ORDER BY name", 
            (district,)
        )
        return [
            {
                'id': row[0],
                'name': row[1],
                'url': row[2],
                'district': row[3]
            }
            for row in results
        ]