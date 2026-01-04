# Farmer-wise table extraction

from bs4 import BeautifulSoup
from ..core.constants import DATE_FORMAT
from datetime import datetime

def parse_farmer_details(html_content):
    """
    Parses the farmer details page and extracts farmer transaction data.
    
    Returns:
        dict: Dictionary containing date and list of farmer transactions
    """
    soup = BeautifulSoup(html_content, 'lxml')
    result = {
        'date': None,
        'transactions': []
    }
    
    # Extract date from header
    header_div = soup.find('div', {'id': 'ctl00_ContentPlaceHolder1_PnlHeader'})
    if header_div:
        header_text = header_div.get_text(strip=True)
        # Extract date from the header text
        # Looking for pattern like "क्रय दिनांक: 02/01/2026"
        if 'क्रय दिनांक:' in header_text:
            parts = header_text.split('क्रय दिनांक:')
            if len(parts) > 1:
                date_str = parts[1].split()[0].strip()  # Get the first part which should be the date
                try:
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                    result['date'] = date_obj.strftime(DATE_FORMAT)
                except ValueError:
                    print(f"Warning: Invalid date format: {date_str}")
    
    # Find the table containing farmer details
    # The table has id 'tblSample' instead of 'ctl00_ContentPlaceHolder1_gvFarmerDetails'
    table = soup.find('table', {'id': 'tblSample'})
    if not table:
        print("Warning: Could not find farmer details table")
        return result
    
    # Extract rows from the table
    rows = table.find_all('tr')
    
    # Find the header row (contains column names)
    header_row_index = None
    for i, row in enumerate(rows):
        cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if 'किसान का नाम' in ''.join(cells):  # 'Farmer Name' in Hindi
            header_row_index = i
            break
    
    # If we found the header row, data rows start after the next row (which contains column numbers)
    if header_row_index is not None:
        data_start_index = header_row_index + 2  # Skip header row and column number row
    else:
        # Fallback to original logic
        data_start_index = 8  # Based on our observation
    
    # Process data rows
    for i in range(data_start_index, len(rows)):
        row = rows[i]
        cells = row.find_all('td')
        
        # Skip the last row which contains totals
        if i == len(rows) - 1:
            continue
            
        # Based on the structure, we need at least 7 cells (0-indexed)
        # Columns: Serial No., Farmer ID, Farmer Name, Address, Quantity, Amount, Transaction Time
        if len(cells) >= 7:
            # Extract farmer registration/ID (column 1) - masked
            farmer_id = cells[1].get_text(strip=True)
            
            # Extract farmer name (column 2)
            farmer_name = cells[2].get_text(strip=True)
            
            # Extract village/address (column 3)
            village = cells[3].get_text(strip=True)
            
            # Extract quantity (column 4)
            quantity_str = cells[4].get_text(strip=True)
            try:
                quantity = float(''.join(c for c in quantity_str if c.isdigit() or c == '.'))
            except ValueError:
                quantity = 0.0
            
            # Extract amount (column 5)
            amount_str = cells[5].get_text(strip=True)
            try:
                # Remove currency symbol and commas
                amount = float(''.join(c for c in amount_str if c.isdigit() or c == '.'))
            except ValueError:
                amount = 0.0
            
            # Extract transaction time (column 6)
            transaction_time = cells[6].get_text(strip=True)
            
            result['transactions'].append({
                'farmer_id': farmer_id,
                'farmer_name': farmer_name,
                'village': village,
                'quantity': quantity,
                'amount': amount,
                'transaction_time': transaction_time
            })
    
    return result