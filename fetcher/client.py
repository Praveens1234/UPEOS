# HTTP GET wrapper with rate limiting

import time
import requests
from .session import create_session
from ..config.settings import Settings

class HTTPClient:
    """
    HTTP client with rate limiting for fetching web pages.
    """
    
    def __init__(self):
        self.session = create_session()
        self.settings = Settings()
        self.last_request_time = 0
    
    def get(self, url):
        """
        Performs a GET request with rate limiting.
        """
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        request_delay = self.settings.request_delay or 1.0  # Default to 1.0 if None
        
        if elapsed < request_delay:
            time.sleep(request_delay - elapsed)
        
        try:
            response = self.session.get(url)
            self.last_request_time = time.time()
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            raise
    
    def close(self):
        """
        Closes the session.
        """
        self.session.close()