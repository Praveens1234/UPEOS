# Export orchestration

import os
import json
from datetime import datetime
from .pdf_builder import PDFBuilder
from ..db.repositories.farmer_repo import FarmerRepository
from ..db.repositories.summary_repo import SummaryRepository
from ..config.settings import Settings

class Exporter:
    """
    Orchestrates the export of data to various formats, primarily PDF.
    """
    
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.pdf_builder = PDFBuilder()
        self.farmer_repo = FarmerRepository(db_connection)
        self.summary_repo = SummaryRepository(db_connection)
        self.settings = Settings()
        
        # Ensure creports.json exists
        if not os.path.exists(self.settings.creport_registry):
            with open(self.settings.creport_registry, 'w') as f:
                json.dump([], f)
    
    def export_transactions_detailed(self, centre_id=None, date=None, from_date=None, to_date=None):
        """
        Exports detailed farmer transaction data to PDF.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            date (str, optional): Specific date in DD/MM/YYYY format
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            dict: Export result with file path and upload info
        """
        # Get transactions from database
        transactions = self._get_transactions(centre_id, date, from_date, to_date)
        
        # Get centre name if filtering by centre
        centre_name = None
        if centre_id:
            from ..db.repositories.centre_repo import CentreRepository
            centre_repo = CentreRepository(self.db_connection)
            centre = centre_repo.get_centre_by_name(centre_id)
            if centre:
                centre_name = centre['name']
        
        # Get date range for report
        date_range = None
        if from_date and to_date:
            date_range = (from_date, to_date)
        elif date:
            date_range = (date, date)
        
        # Generate PDF
        pdf_path = self.pdf_builder.generate_transaction_report(transactions, centre_name, date_range)
        
        # Register the report
        report_info = {
            'type': 'detailed_transactions',
            'generated_at': datetime.now().isoformat(),
            'file_path': pdf_path,
            'centre_id': centre_id,
            'centre_name': centre_name,
            'date': date,
            'from_date': from_date,
            'to_date': to_date
        }
        
        self._register_report(report_info)
        
        return {
            'status': 'success',
            'file_path': pdf_path,
            'report_info': report_info
        }
    
    def export_daywise_statement(self, centre_id=None, from_date=None, to_date=None):
        """
        Exports day-wise summary data to PDF.
        
        Args:
            centre_id (int, optional): Centre ID to filter by
            from_date (str, optional): Start date in DD/MM/YYYY format
            to_date (str, optional): End date in DD/MM/YYYY format
            
        Returns:
            dict: Export result with file path and upload info
        """
        # Get summaries from database
        summaries = self._get_summaries(centre_id, from_date, to_date)
        
        # Get centre name if filtering by centre
        centre_name = None
        if centre_id:
            from ..db.repositories.centre_repo import CentreRepository
            centre_repo = CentreRepository(self.db_connection)
            centre = centre_repo.get_centre_by_name(centre_id)
            if centre:
                centre_name = centre['name']
        
        # Get date range for report
        date_range = None
        if from_date and to_date:
            date_range = (from_date, to_date)
        
        # Generate PDF
        pdf_path = self.pdf_builder.generate_summary_report(summaries, centre_name, date_range)
        
        # Register the report
        report_info = {
            'type': 'daywise_summary',
            'generated_at': datetime.now().isoformat(),
            'file_path': pdf_path,
            'centre_id': centre_id,
            'centre_name': centre_name,
            'from_date': from_date,
            'to_date': to_date
        }
        
        self._register_report(report_info)
        
        return {
            'status': 'success',
            'file_path': pdf_path,
            'report_info': report_info
        }
    
    def _get_transactions(self, centre_id=None, date=None, from_date=None, to_date=None):
        """
        Retrieves transactions from the database based on filters.
        """
        # This is a simplified implementation
        # In a full implementation, we would build a proper query
        query = """
        SELECT ft.id, ft.centre_id, ft.date, ft.farmer_id, ft.farmer_name, 
               ft.village, ft.quantity, ft.amount, ft.transaction_time
        FROM farmer_transactions ft
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND ft.centre_id = ?"
            params.append(centre_id)
        
        if date:
            query += " AND ft.date = ?"
            params.append(date)
        
        if from_date:
            query += " AND ft.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND ft.date <= ?"
            params.append(to_date)
        
        query += " ORDER BY ft.date, ft.farmer_name"
        
        results = self.db_connection.execute_query(query, params)
        
        return [
            {
                'id': row[0],
                'centre_id': row[1],
                'date': row[2],
                'farmer_id': row[3],
                'farmer_name': row[4],
                'village': row[5],
                'quantity': row[6],
                'amount': row[7],
                'transaction_time': row[8]
            }
            for row in results
        ]
    
    def _get_summaries(self, centre_id=None, from_date=None, to_date=None):
        """
        Retrieves summaries from the database based on filters.
        """
        # This is a simplified implementation
        # In a full implementation, we would build a proper query
        query = """
        SELECT dws.date, dws.farmer_count, dws.quantity, dws.amount
        FROM datewise_summaries dws
        WHERE 1=1
        """
        params = []
        
        if centre_id:
            query += " AND dws.centre_id = ?"
            params.append(centre_id)
        
        if from_date:
            query += " AND dws.date >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND dws.date <= ?"
            params.append(to_date)
        
        query += " ORDER BY dws.date"
        
        results = self.db_connection.execute_query(query, params)
        
        return [
            {
                'date': row[0],
                'farmer_count': row[1],
                'quantity': row[2],
                'amount': row[3]
            }
            for row in results
        ]
    
    def _register_report(self, report_info):
        """
        Registers a generated report in the creports.json file.
        """
        # Read existing reports
        with open(self.settings.creport_registry, 'r') as f:
            reports = json.load(f)
        
        # Add new report
        reports.append(report_info)
        
        # Write back to file
        with open(self.settings.creport_registry, 'w') as f:
            json.dump(reports, f, indent=2)
    
    def list_generated_reports(self):
        """
        Lists all generated reports.
        
        Returns:
            list: List of report information dictionaries
        """
        with open(self.settings.creport_registry, 'r') as f:
            return json.load(f)
    
    def get_report_info(self, file_path):
        """
        Gets information about a specific report.
        
        Args:
            file_path (str): Path to the report file
            
        Returns:
            dict: Report information or None if not found
        """
        reports = self.list_generated_reports()
        for report in reports:
            if report.get('file_path') == file_path:
                return report
        return None