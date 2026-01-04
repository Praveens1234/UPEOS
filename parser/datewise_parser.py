# Date-wise summary extraction

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from ..core.constants import DATE_FORMAT
from datetime import datetime

def parse_datewise_summary(html_content, base_url):
    """
    Parses the date-wise summary page and extracts date-wise procurement data.
    
    Returns:
        dict: Dictionary containing centre information and list of date-wise summaries
    """
    soup = BeautifulSoup(html_content, 'lxml')
    result = {
        'centre_name': None,
        'dates': []
    }
    
    # Extract centre name from the header
    header_div = soup.find('div', {'id': 'ctl00_ContentPlaceHolder1_PnlHeader'})
    if header_div:
        header_text = header_div.get_text(strip=True)
        # Extract centre name from the header text
        # Looking for pattern like "क्रय केंद्र का नाम :  UPSSखागा मंडी - खागा नगर पंचायत"
        if 'क्रय केंद्र का नाम :' in header_text:
            parts = header_text.split('क्रय केंद्र का नाम :')
            if len(parts) > 1:
                centre_name = parts[1].split('जनपद :')[0].strip()
                result['centre_name'] = centre_name
    
    # Find the table containing date-wise summary
    # The table has id 'tblSample' instead of 'ctl00_ContentPlaceHolder1_gvDateWise'
    table = soup.find('table', {'id': 'tblSample'})
    if not table:
        print("Warning: Could not find date-wise summary table")
        return result
    
    # Extract rows from the table
    rows = table.find_all('tr')
    
    # Find the header row (contains column names)
    header_row_index = None
    for i, row in enumerate(rows):
        cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if 'तिथि' in ''.join(cells):  # 'Date' in Hindi
            header_row_index = i
            break
    
    # If we found the header row, data rows start after the next row (which contains column numbers)
    if header_row_index is not None:
        data_start_index = header_row_index + 2  # Skip header row and column number row
    else:
        # Fallback to original logic
        data_start_index = 10  # Based on our observation
    
    # Process data rows
    for i in range(data_start_index, len(rows)):
        row = rows[i]
        cells = row.find_all('td')
        
        # Skip the last row which contains totals
        if i == len(rows) - 1:
            continue
            
        # Based on the structure, we need at least 5 cells (0-indexed)
        # Columns: Serial No., Date, Farmer Count, Quantity, Amount
        if len(cells) >= 5:
            # Extract date (column 1)
            date_str = cells[1].get_text(strip=True)
            try:
                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                formatted_date = date_obj.strftime(DATE_FORMAT)
            except ValueError:
                print(f"Warning: Invalid date format: {date_str}")
                continue
            
            # Extract official farmer count (column 2)
            farmer_count_str = cells[2].get_text(strip=True)
            try:
                farmer_count = int(farmer_count_str)
            except ValueError:
                farmer_count = 0
            
            # Extract total quantity (column 3)
            quantity_str = cells[3].get_text(strip=True)
            try:
                # Remove any non-numeric characters except decimal point
                quantity = float(''.join(c for c in quantity_str if c.isdigit() or c == '.'))
            except ValueError:
                quantity = 0.0
            
            # Extract total amount (column 4)
            amount_str = cells[4].get_text(strip=True)
            try:
                # Remove currency symbol and commas
                amount = float(''.join(c for c in amount_str if c.isdigit() or c == '.'))
            except ValueError:
                amount = 0.0
            
            # Extract link to farmer details (if exists)
            farmer_details_url = None
            date_link = cells[1].find('a')
            if date_link:
                relative_url = date_link.get('href')
                farmer_details_url = urljoin(base_url, relative_url)
            
            result['dates'].append({
                'date': formatted_date,
                'farmer_count': farmer_count,
                'quantity': quantity,
                'amount': amount,
                'details_url': farmer_details_url
            })
    
    return result