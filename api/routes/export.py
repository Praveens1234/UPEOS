# Export API routes

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from ...db.connection import DatabaseConnection
from ...export.exporter import Exporter
from ...export.uploader import ReportUploader

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

@router.get("/export/transactions/detailed")
async def export_transactions_detailed(
    centre_id: Optional[int] = Query(None, description="Centre ID to filter by"),
    date: Optional[str] = Query(None, description="Specific date in DD/MM/YYYY format"),
    from_date: Optional[str] = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: Optional[str] = Query(None, description="End date in DD/MM/YYYY format"),
    upload: bool = Query(False, description="Whether to upload the report to cloud storage"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Exports detailed farmer transaction data to PDF.
    """
    exporter = Exporter(db)
    
    try:
        result = exporter.export_transactions_detailed(centre_id, date, from_date, to_date)
        
        if upload:
            uploader = ReportUploader()
            upload_result = uploader.upload_and_register_report(result['file_path'])
            result['upload'] = upload_result
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/export/summary/daywise")
async def export_daywise_statement(
    centre_id: Optional[int] = Query(None, description="Centre ID to filter by"),
    from_date: Optional[str] = Query(None, description="Start date in DD/MM/YYYY format"),
    to_date: Optional[str] = Query(None, description="End date in DD/MM/YYYY format"),
    upload: bool = Query(False, description="Whether to upload the report to cloud storage"),
    db: DatabaseConnection = Depends(get_db)
):
    """
    Exports day-wise summary data to PDF.
    """
    exporter = Exporter(db)
    
    try:
        result = exporter.export_daywise_statement(centre_id, from_date, to_date)
        
        if upload:
            uploader = ReportUploader()
            upload_result = uploader.upload_and_register_report(result['file_path'])
            result['upload'] = upload_result
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

@router.get("/export/reports")
async def list_generated_reports(db: DatabaseConnection = Depends(get_db)):
    """
    Lists all generated reports.
    """
    exporter = Exporter(db)
    reports = exporter.list_generated_reports()
    return {"reports": reports}

@router.get("/export/reports/{file_path}")
async def get_report_info(file_path: str, db: DatabaseConnection = Depends(get_db)):
    """
    Gets information about a specific report.
    """
    exporter = Exporter(db)
    report_info = exporter.get_report_info(file_path)
    
    if not report_info:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {"report": report_info}