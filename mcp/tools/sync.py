# Sync MCP tools

from ...db.connection import DatabaseConnection
from ...sync.engine import SyncEngine

def sync_all_centres():
    """
    Synchronizes all centres from the government website.
    
    Returns:
        dict: Dictionary containing sync result
    """
    db = DatabaseConnection()
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_all_centres()
        return {"message": f"Synced {count} centres", "centres_synced": count}
    except Exception as e:
        return {"error": f"Synchronization failed: {str(e)}"}
    finally:
        sync_engine.close()
        db.close()

def sync_centre(centre_name: str):
    """
    Synchronizes date-wise data for a specific centre.
    
    Args:
        centre_name (str): Name of the centre to sync
        
    Returns:
        dict: Dictionary containing sync result
    """
    db = DatabaseConnection()
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_centre_datewise_data(centre_name)
        return {"message": f"Synced {count} date-wise entries for centre {centre_name}", "entries_synced": count}
    except Exception as e:
        return {"error": f"Synchronization failed: {str(e)}"}
    finally:
        sync_engine.close()
        db.close()

def sync_centre_date(centre_name: str, date: str):
    """
    Synchronizes farmer details for a specific centre and date.
    
    Args:
        centre_name (str): Name of the centre
        date (str): Date in DD/MM/YYYY format
        
    Returns:
        dict: Dictionary containing sync result
    """
    db = DatabaseConnection()
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_farmer_details(centre_name, date)
        return {"message": f"Synced {count} farmer transactions for centre {centre_name} on date {date}", "transactions_synced": count}
    except Exception as e:
        return {"error": f"Synchronization failed: {str(e)}"}
    finally:
        sync_engine.close()
        db.close()