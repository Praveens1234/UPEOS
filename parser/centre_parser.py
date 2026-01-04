# Centre list extraction

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_centre_list(html_content, base_url):
    """
    Parses the centre list page and extracts centre information.
    
    Returns:
        list: List of dictionaries containing centre information
    """
    soup = BeautifulSoup(html_content, 'lxml')
    centres = []
    
    # Find the table containing centre information
    # The table has id 'tblSample' instead of 'ctl00_ContentPlaceHolder1_gvCenterName'
    table = soup.find('table', {'id': 'tblSample'})
    if not table:
        print("Warning: Could not find centre list table")
        return centres
    
    # Extract rows from the table
    # Based on the structure, the actual data starts from row 10 (index 9)
    # Rows 7-9 contain headers, and row 10 onwards contain data
    rows = table.find_all('tr')
    
    # Find the header row (contains column names)
    header_row_index = None
    for i, row in enumerate(rows):
        cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
        if 'क्रय केंद्र का नाम' in ''.join(cells):  # 'Name of Purchase Center' in Hindi
            header_row_index = i
            break
    
    # If we found the header row, data rows start after the next row (which contains column numbers)
    if header_row_index is not None:
        data_start_index = header_row_index + 2  # Skip header row and column number row
    else:
        # Fallback to original logic
        data_start_index = 9  # Based on our observation
    
    # Process data rows
    for i in range(data_start_index, len(rows)):
        row = rows[i]
        cells = row.find_all('td')
        
        # Skip the last row which contains totals
        if i == len(rows) - 1:
            continue
            
        # Based on the structure, we need at least 6 cells (0-indexed)
        if len(cells) >= 6:
            # Extract centre name and link (column 1)
            name_cell = cells[1]
            link_tag = name_cell.find('a')
            
            if link_tag:
                centre_name = link_tag.get_text(strip=True)
                relative_url = link_tag.get('href')
                absolute_url = urljoin(base_url, relative_url)
                
                centres.append({
                    'name': centre_name,
                    'url': absolute_url
                })
    
    return centres