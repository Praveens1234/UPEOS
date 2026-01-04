# Search API routes

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from ...db.connection import DatabaseConnection
from ...search.engine import SearchEngine

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

@router.get("/search/farmer")
async def search_farmer(
    farmer_name: str = Query(..., description="Farmer name or partial name to search for"),
    village: Optional[str] = Query(None, description="Village name or partial name to filter by"),
    min_quantity: Optional[float] = Query(None, description="Minimum quantity filter"),
    max_quantity: Optional[float] = Query(None, description="Maximum quantity filter"),
    min_amount: Optional[float] = Query(None, description="Minimum amount filter"),
    max_amount: Optional[float] = Query(None, description="Maximum amount filter"),
    from_date: Optional[str] = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: Optional[str] = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Searches for farmer transactions based on various criteria.
    """
    search_engine = SearchEngine(db)
    
    filters = {
        'farmer_name': farmer_name
    }
    
    if village:
        filters['village'] = village
    if min_quantity is not None:
        filters['min_quantity'] = min_quantity
    if max_quantity is not None:
        filters['max_quantity'] = max_quantity
    if min_amount is not None:
        filters['min_amount'] = min_amount
    if max_amount is not None:
        filters['max_amount'] = max_amount
    if from_date:
        filters['from_date'] = from_date
    if to_date:
        filters['to_date'] = to_date
    
    result = search_engine.search_farmers(filters)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['errors'])
    
    return {"results": result['data']}

@router.get("/search/village")
async def search_by_village(
    village: str = Query(..., description="Village name or partial name to search for"),
    from_date: Optional[str] = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: Optional[str] = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Searches for villages matching the given criteria.
    """
    search_engine = SearchEngine(db)
    
    filters = {
        'village': village
    }
    
    if from_date:
        filters['from_date'] = from_date
    if to_date:
        filters['to_date'] = to_date
    
    result = search_engine.search_by_village(filters)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['errors'])
    
    return {"results": result['data']}

@router.get("/search/advanced")
async def advanced_search(
    farmer_name: Optional[str] = Query(None, description="Farmer name or partial name to search for"),
    village: Optional[str] = Query(None, description="Village name or partial name to filter by"),
    min_quantity: Optional[float] = Query(None, description="Minimum quantity filter"),
    max_quantity: Optional[float] = Query(None, description="Maximum quantity filter"),
    min_amount: Optional[float] = Query(None, description="Minimum amount filter"),
    max_amount: Optional[float] = Query(None, description="Maximum amount filter"),
    from_date: Optional[str] = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: Optional[str] = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Performs an advanced search with multiple criteria.
    """
    search_engine = SearchEngine(db)
    
    filters = {}
    
    if farmer_name:
        filters['farmer_name'] = farmer_name
    if village:
        filters['village'] = village
    if min_quantity is not None:
        filters['min_quantity'] = min_quantity
    if max_quantity is not None:
        filters['max_quantity'] = max_quantity
    if min_amount is not None:
        filters['min_amount'] = min_amount
    if max_amount is not None:
        filters['max_amount'] = max_amount
    if from_date:
        filters['from_date'] = from_date
    if to_date:
        filters['to_date'] = to_date
    
    result = search_engine.advanced_search(filters)
    
    if result['status'] == 'error':
        raise HTTPException(status_code=400, detail=result['errors'])
    
    return {"results": result['data']}