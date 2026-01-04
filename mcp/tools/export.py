# Export MCP tools

from typing import Optional
from ...db.connection import DatabaseConnection
from ...export.exporter import Exporter
from ...export.uploader import ReportUploader

def export_transactions_detailed(
    centre_id: Optional[int] = None,
    date: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    upload: bool = False
):
    """
    Exports detailed farmer transaction data to PDF.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        date (str, optional): Specific date in DD/MM/YYYY format
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        upload (bool): Whether to upload the report to cloud storage
        
    Returns:
        dict: Dictionary containing export result
    """
    db = DatabaseConnection()
    try:
        exporter = Exporter(db)
        result = exporter.export_transactions_detailed(centre_id, date, from_date, to_date)
        
        if upload:
            uploader = ReportUploader()
            upload_result = uploader.upload_and_register_report(result['file_path'])
            result['upload'] = upload_result
        
        return result
    except Exception as e:
        return {"error": f"Export failed: {str(e)}"}
    finally:
        db.close()

def export_daywise_statement(
    centre_id: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    upload: bool = False
):
    """
    Exports day-wise summary data to PDF.
    
    Args:
        centre_id (int, optional): Centre ID to filter by
        from_date (str, optional): Start date in DD/MM/YYYY format
        to_date (str, optional): End date in DD/MM/YYYY format
        upload (bool): Whether to upload the report to cloud storage
        
    Returns:
        dict: Dictionary containing export result
    """
    db = DatabaseConnection()
    try:
        exporter = Exporter(db)
        result = exporter.export_daywise_statement(centre_id, from_date, to_date)
        
        if upload:
            uploader = ReportUploader()
            upload_result = uploader.upload_and_register_report(result['file_path'])
            result['upload'] = upload_result
        
        return result
    except Exception as e:
        return {"error": f"Export failed: {str(e)}"}
    finally:
        db.close()

def list_generated_reports():
    """
    Lists all generated reports.
    
    Returns:
        dict: Dictionary containing list of reports
    """
    db = DatabaseConnection()
    try:
        exporter = Exporter(db)
        reports = exporter.list_generated_reports()
        return {"reports": reports}
    except Exception as e:
        return {"error": f"Failed to list reports: {str(e)}"}
    finally:
        db.close()

def get_report_info(file_path: str):
    """
    Gets information about a specific report.
    
    Args:
        file_path (str): Path to the report file
        
    Returns:
        dict: Dictionary containing report information
    """
    db = DatabaseConnection()
    try:
        exporter = Exporter(db)
        report_info = exporter.get_report_info(file_path)
        
        if not report_info:
            return {"error": "Report not found"}
        
        return {"report": report_info}
    except Exception as e:
        return {"error": f"Failed to get report info: {str(e)}"}
    finally:
        db.close()