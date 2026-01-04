# reportlab PDF generation

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.flowables import HRFlowable
from .layouts import (
    PAGE_SIZE, MARGIN_LEFT, MARGIN_RIGHT, MARGIN_TOP, MARGIN_BOTTOM,
    get_table_style, get_totals_table_style, get_title_style, get_heading_style, 
    get_subheading_style, get_normal_style, get_info_style, TRANSACTION_TABLE_WIDTHS, 
    SUMMARY_TABLE_WIDTHS, get_footer_text
)
from ..config.settings import Settings

class PDFBuilder:
    """
    Builds professional PDF reports using reportlab.
    """
    
    def __init__(self):
        self.settings = Settings()
        self.styles = getSampleStyleSheet()
        
        # Ensure reports directory exists
        os.makedirs(self.settings.report_directory, exist_ok=True)
    
    def format_currency(self, amount):
        """
        Format amount as Indian Rupee currency.
        """
        if amount is None:
            return "₹0.00"
        return f"₹{amount:,.2f}"
    
    def format_quantity(self, quantity):
        """
        Format quantity with proper units.
        """
        if quantity is None:
            return "0.00"
        return f"{quantity:.2f}"
    
    def generate_transaction_report(self, transactions, centre_name=None, date_range=None):
        """
        Generates a detailed transaction report with professional formatting.
        
        Args:
            transactions (list): List of transaction dictionaries
            centre_name (str, optional): Name of the centre
            date_range (tuple, optional): Tuple of (from_date, to_date)
            
        Returns:
            str: Path to the generated PDF file
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transaction_report_{timestamp}.pdf"
        filepath = os.path.join(self.settings.report_directory, filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=PAGE_SIZE,
            leftMargin=MARGIN_LEFT,
            rightMargin=MARGIN_RIGHT,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM
        )
        
        # Build content
        story = []
        
        # Title
        title = "UPEOS - Detailed Transaction Report"
        story.append(Paragraph(title, get_title_style()))
        story.append(Spacer(1, 12))
        
        # Report info section
        story.append(Paragraph("Report Information", get_heading_style()))
        
        # Centre information
        if centre_name:
            story.append(Paragraph(f"<b>Centre:</b> {centre_name}", get_normal_style()))
        
        # Date range information
        if date_range:
            story.append(Paragraph(f"<b>Date Range:</b> {date_range[0]} to {date_range[1]}", get_normal_style()))
        elif transactions:
            # If no date range specified, show the date range from the data
            dates = [tx.get('date') for tx in transactions if tx.get('date')]
            if dates:
                min_date = min(dates)
                max_date = max(dates)
                story.append(Paragraph(f"<b>Date Range:</b> {min_date} to {max_date}", get_normal_style()))
        
        # Generation timestamp
        story.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", get_normal_style()))
        story.append(Spacer(1, 12))
        
        # Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=10, spaceAfter=10))
        
        # Summary statistics
        if transactions:
            total_quantity = sum(tx.get('quantity', 0) for tx in transactions)
            total_amount = sum(tx.get('amount', 0) for tx in transactions)
            total_transactions = len(transactions)
            
            story.append(Paragraph("Summary Statistics", get_subheading_style()))
            story.append(Paragraph(f"<b>Total Transactions:</b> {total_transactions}", get_normal_style()))
            story.append(Paragraph(f"<b>Total Quantity:</b> {self.format_quantity(total_quantity)} MT", get_normal_style()))
            story.append(Paragraph(f"<b>Total Amount:</b> {self.format_currency(total_amount)}", get_normal_style()))
            story.append(Spacer(1, 12))
        
        # Table data
        if transactions:
            story.append(Paragraph("Transaction Details", get_heading_style()))
            
            table_data = [
                ["#", "Farmer ID", "Farmer Name", "Village", "Quantity (MT)", "Amount (₹)", "Time"]
            ]
            
            for i, transaction in enumerate(transactions, 1):
                table_data.append([
                    str(i),
                    transaction.get('farmer_id', ''),
                    transaction.get('farmer_name', ''),
                    transaction.get('village', ''),
                    self.format_quantity(transaction.get('quantity')),
                    self.format_currency(transaction.get('amount')),
                    transaction.get('transaction_time', '')
                ])
            
            # Create table
            table = Table(table_data, colWidths=TRANSACTION_TABLE_WIDTHS)
            table.setStyle(get_table_style())
            story.append(table)
        else:
            story.append(Paragraph("No transactions found for the specified criteria.", get_normal_style()))
        
        # Footer
        story.append(PageBreak())
        story.append(Paragraph(get_footer_text(), get_info_style()))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_summary_report(self, summaries, centre_name=None, date_range=None):
        """
        Generates a professional day-wise summary report.
        
        Args:
            summaries (list): List of summary dictionaries
            centre_name (str, optional): Name of the centre
            date_range (tuple, optional): Tuple of (from_date, to_date)
            
        Returns:
            str: Path to the generated PDF file
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"summary_report_{timestamp}.pdf"
        filepath = os.path.join(self.settings.report_directory, filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=PAGE_SIZE,
            leftMargin=MARGIN_LEFT,
            rightMargin=MARGIN_RIGHT,
            topMargin=MARGIN_TOP,
            bottomMargin=MARGIN_BOTTOM
        )
        
        # Build content
        story = []
        
        # Title
        title = "UPEOS - Day-wise Summary Report"
        story.append(Paragraph(title, get_title_style()))
        story.append(Spacer(1, 12))
        
        # Report info section
        story.append(Paragraph("Report Information", get_heading_style()))
        
        # Centre information
        if centre_name:
            story.append(Paragraph(f"<b>Centre:</b> {centre_name}", get_normal_style()))
        
        # Date range information
        if date_range:
            story.append(Paragraph(f"<b>Date Range:</b> {date_range[0]} to {date_range[1]}", get_normal_style()))
        elif summaries:
            # If no date range specified, show the date range from the data
            dates = [summary.get('date') for summary in summaries if summary.get('date')]
            if dates:
                min_date = min(dates)
                max_date = max(dates)
                story.append(Paragraph(f"<b>Date Range:</b> {min_date} to {max_date}", get_normal_style()))
        
        # Generation timestamp
        story.append(Paragraph(f"<b>Generated on:</b> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", get_normal_style()))
        story.append(Spacer(1, 12))
        
        # Separator
        story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey, spaceBefore=10, spaceAfter=10))
        
        # Summary statistics
        if summaries:
            total_farmers = sum(summary.get('farmer_count', 0) for summary in summaries)
            total_quantity = sum(summary.get('quantity', 0) for summary in summaries)
            total_amount = sum(summary.get('amount', 0) for summary in summaries)
            total_days = len(summaries)
            
            story.append(Paragraph("Summary Statistics", get_subheading_style()))
            story.append(Paragraph(f"<b>Total Days:</b> {total_days}", get_normal_style()))
            story.append(Paragraph(f"<b>Total Farmers:</b> {total_farmers}", get_normal_style()))
            story.append(Paragraph(f"<b>Total Quantity:</b> {self.format_quantity(total_quantity)} MT", get_normal_style()))
            story.append(Paragraph(f"<b>Total Amount:</b> {self.format_currency(total_amount)}", get_normal_style()))
            story.append(Spacer(1, 12))
        
        # Table data
        if summaries:
            story.append(Paragraph("Day-wise Summary", get_heading_style()))
            
            table_data = [
                ["#", "Date", "Farmers", "Quantity (MT)", "Amount (₹)"]
            ]
            
            for i, summary in enumerate(summaries, 1):
                table_data.append([
                    str(i),
                    summary.get('date', ''),
                    str(summary.get('farmer_count', '')),
                    self.format_quantity(summary.get('quantity')),
                    self.format_currency(summary.get('amount'))
                ])
            
            # Add totals row
            total_farmers = sum(summary.get('farmer_count', 0) for summary in summaries)
            total_quantity = sum(summary.get('quantity', 0) for summary in summaries)
            total_amount = sum(summary.get('amount', 0) for summary in summaries)
            
            table_data.append([
                "",  # Empty cell for #
                "TOTAL",
                str(total_farmers),
                self.format_quantity(total_quantity),
                self.format_currency(total_amount)
            ])
            
            # Create table
            table = Table(table_data, colWidths=[0.5*inch, 1.0*inch, 0.9*inch, 1.0*inch, 1.2*inch])
            
            # Apply regular table style first
            table.setStyle(get_table_style())
            
            # Apply special style for totals row
            table.setStyle(get_totals_table_style())
            
            story.append(table)
        else:
            story.append(Paragraph("No summary data found for the specified criteria.", get_normal_style()))
        
        # Footer
        story.append(PageBreak())
        story.append(Paragraph(get_footer_text(), get_info_style()))
        
        # Build PDF
        doc.build(story)
        return filepath