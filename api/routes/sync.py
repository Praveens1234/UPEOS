# Synchronization API routes

from fastapi import APIRouter, Depends, HTTPException
from ...db.connection import DatabaseConnection
from ...sync.engine import SyncEngine

router = APIRouter()

def get_db():
    """
    Dependency to get database connection.
    """
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()

@router.post("/sync/all-centres")
async def sync_all_centres(db: DatabaseConnection = Depends(get_db)):
    """
    Synchronizes all centres from the government website.
    """
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_all_centres()
        return {"message": f"Synced {count} centres", "centres_synced": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synchronization failed: {str(e)}")
    finally:
        sync_engine.close()

@router.post("/sync/centre/{centre_name}")
async def sync_centre(centre_name: str, db: DatabaseConnection = Depends(get_db)):
    """
    Synchronizes date-wise data for a specific centre.
    """
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_centre_datewise_data(centre_name)
        return {"message": f"Synced {count} date-wise entries for centre {centre_name}", "entries_synced": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synchronization failed: {str(e)}")
    finally:
        sync_engine.close()

@router.post("/sync/centre/{centre_name}/date/{date}")
async def sync_centre_date(centre_name: str, date: str, db: DatabaseConnection = Depends(get_db)):
    """
    Synchronizes farmer details for a specific centre and date.
    """
    sync_engine = SyncEngine(db)
    try:
        count = sync_engine.sync_farmer_details(centre_name, date)
        return {"message": f"Synced {count} farmer transactions for centre {centre_name} on date {date}", "transactions_synced": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synchronization failed: {str(e)}")
    finally:
        sync_engine.close()