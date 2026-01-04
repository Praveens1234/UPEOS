# Discovery API routes

from fastapi import APIRouter, Depends
from ...db.connection import DatabaseConnection
from ...db.repositories.centre_repo import CentreRepository

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

@router.get("/centres")
async def list_centres(db: DatabaseConnection = Depends(get_db)):
    """
    Lists all procurement centres.
    """
    centre_repo = CentreRepository(db)
    centres = centre_repo.get_all_centres()
    return {"centres": centres}

@router.get("/centres/{centre_name}")
async def get_centre(centre_name: str, db: DatabaseConnection = Depends(get_db)):
    """
    Gets details of a specific centre by name.
    """
    centre_repo = CentreRepository(db)
    centre = centre_repo.get_centre_by_name(centre_name)
    
    if not centre:
        raise HTTPException(status_code=404, detail="Centre not found")
    
    return {"centre": centre}

@router.get("/districts/{district_name}/centres")
async def list_centres_by_district(district_name: str, db: DatabaseConnection = Depends(get_db)):
    """
    Lists all procurement centres in a specific district.
    """
    centre_repo = CentreRepository(db)
    centres = centre_repo.get_centres_by_district(district_name)
    return {"centres": centres}