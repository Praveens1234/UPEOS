# requests.Session creation & headers

import requests
from ..core.constants import BASE_URL

def create_session():
    """
    Creates a requests.Session with appropriate headers for mimicking a real browser.
    """
    session = requests.Session()
    
    # Set headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Perform initial request to establish session
    try:
        session.get(BASE_URL)
    except Exception as e:
        print(f"Warning: Failed to establish initial session: {e}")
    
    return session