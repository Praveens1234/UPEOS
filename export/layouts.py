# Table & page layouts

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts (if available)
try:
    # Try to register a better font if available
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    FONT_NAME = 'Arial'
except:
    FONT_NAME = 'Helvetica'

# Page size and margins
PAGE_SIZE = A4
MARGIN_LEFT = 0.75 * inch
MARGIN_RIGHT = 0.75 * inch
MARGIN_TOP = 0.75 * inch
MARGIN_BOTTOM = 0.75 * inch

# Color scheme for professional look
PRIMARY_COLOR = colors.HexColor('#2C3E50')  # Dark blue
SECONDARY_COLOR = colors.HexColor('#3498DB')  # Light blue
ACCENT_COLOR = colors.HexColor('#E74C3C')  # Red
LIGHT_BG = colors.HexColor('#ECF0F1')  # Light gray
HEADER_BG = colors.HexColor('#34495E')  # Darker blue

# Table styles
def get_table_style():
    """
    Returns a professional table style for reports.
    """
    return TableStyle([
        # Header styling
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_NAME + '-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows styling
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
        
        # Alternate row coloring
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        
        # Hover effect simulation (not actually hover, but visual distinction)
        ('LINEABOVE', (0, 1), (-1, 1), 2, SECONDARY_COLOR),
    ])

def get_totals_table_style():
    """
    Returns a special table style for totals row.
    """
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ACCENT_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), FONT_NAME + '-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
    ])

def get_title_style():
    """
    Returns a style for report titles.
    """
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = FONT_NAME + '-Bold'
    title_style.fontSize = 20
    title_style.textColor = PRIMARY_COLOR
    title_style.spaceAfter = 20
    title_style.alignment = 1  # Center alignment
    return title_style

def get_heading_style():
    """
    Returns a style for report headings.
    """
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.fontName = FONT_NAME + '-Bold'
    heading_style.fontSize = 14
    heading_style.textColor = SECONDARY_COLOR
    heading_style.spaceAfter = 15
    return heading_style

def get_subheading_style():
    """
    Returns a style for report subheadings.
    """
    styles = getSampleStyleSheet()
    heading_style = styles['Heading2']
    heading_style.fontName = FONT_NAME + '-Bold'
    heading_style.fontSize = 12
    heading_style.textColor = PRIMARY_COLOR
    heading_style.spaceAfter = 10
    return heading_style

def get_normal_style():
    """
    Returns a normal text style for report content.
    """
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.fontName = FONT_NAME
    normal_style.fontSize = 10
    normal_style.spaceAfter = 8
    normal_style.leading = 12
    return normal_style

def get_info_style():
    """
    Returns a style for informational text.
    """
    styles = getSampleStyleSheet()
    info_style = styles['Normal']
    info_style.fontName = FONT_NAME
    info_style.fontSize = 9
    info_style.textColor = colors.grey
    info_style.spaceAfter = 4
    return info_style

# Column widths for different table types
TRANSACTION_TABLE_WIDTHS = [
    0.9 * inch,  # Farmer ID
    1.4 * inch,  # Farmer Name
    1.3 * inch,  # Village
    0.8 * inch,  # Quantity
    1.0 * inch,  # Amount
    1.1 * inch   # Transaction Time
]

SUMMARY_TABLE_WIDTHS = [
    1.0 * inch,  # Date
    0.9 * inch,  # Farmer Count
    1.0 * inch,  # Quantity
    1.2 * inch,  # Amount
    1.4 * inch   # Centre Name (not used in single centre reports)
]

# Footer information
def get_footer_text():
    """
    Returns footer text for reports.
    """
    from datetime import datetime
    return f"Generated on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | UPEOS - Uttar Pradesh E-Procurement Service"