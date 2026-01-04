# Statistics API routes

from fastapi import APIRouter, Depends, Query
from ...db.connection import DatabaseConnection
from ...aggregate.stats import StatsAggregator
from ...aggregate.breakdown import BreakdownAggregator

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

@router.get("/stats")
async def get_stats(
    centre_id: int = Query(None, description="Centre ID to filter by"),
    date: str = Query(None, description="Specific date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets comprehensive statistics for a specific centre and/or date.
    """
    aggregator = StatsAggregator(db)
    stats = aggregator.get_stats(centre_id, date)
    return {"stats": stats}

@router.get("/stats/total-quantity")
async def get_total_quantity(
    centre_id: int = Query(None, description="Centre ID to filter by"),
    from_date: str = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: str = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets the total quantity aggregated by centre and/or date range.
    """
    aggregator = StatsAggregator(db)
    total = aggregator.get_total_quantity(centre_id, from_date, to_date)
    return {"total_quantity": total}

@router.get("/stats/total-amount")
async def get_total_amount(
    centre_id: int = Query(None, description="Centre ID to filter by"),
    from_date: str = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: str = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets the total amount aggregated by centre and/or date range.
    """
    aggregator = StatsAggregator(db)
    total = aggregator.get_total_amount(centre_id, from_date, to_date)
    return {"total_amount": total}

@router.get("/stats/total-farmers")
async def get_total_farmers(
    centre_id: int = Query(None, description="Centre ID to filter by"),
    from_date: str = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: str = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets the total farmer count aggregated by centre and/or date range.
    """
    aggregator = StatsAggregator(db)
    total = aggregator.get_total_farmers(centre_id, from_date, to_date)
    return {"total_farmers": total}

@router.get("/stats/daily-breakdown")
async def get_daily_breakdown(
    centre_id: int = Query(None, description="Centre ID to filter by"),
    from_date: str = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: str = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets a date-wise breakdown of procurement data.
    """
    aggregator = BreakdownAggregator(db)
    breakdown = aggregator.get_daily_breakdown(centre_id, from_date, to_date)
    return {"daily_breakdown": breakdown}

@router.get("/stats/centre-comparison")
async def get_centre_comparison(
    date: str = Query(None, description="Specific date in DD/MM/YYYY format"),
    from_date: str = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: str = Query(None, description="End date in DD/MM/YYYY format"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Gets a centre-wise comparison of procurement data.
    """
    aggregator = BreakdownAggregator(db)
    comparison = aggregator.get_centre_comparison(date, from_date, to_date)
    return {"centre_comparison": comparison}