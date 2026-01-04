# Page type detection (centre/date/farmer)

from bs4 import BeautifulSoup

def detect_page_type(html_content):
    """
    Detects the type of page based on its content.
    
    Returns:
        str: One of 'centre_list', 'datewise_summary', 'farmer_details', or 'unknown'
    """
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Check for specific elements that identify each page type
    if soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gvCenterName'}):
        return 'centre_list'
    elif soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gvDateWise'}):
        return 'datewise_summary'
    elif soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gvFarmerDetails'}):
        return 'farmer_details'
    else:
        return 'unknown'