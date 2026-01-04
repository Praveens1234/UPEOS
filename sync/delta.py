# HTML hash comparison

from ..utils.hashing import compute_html_hash

class DeltaChecker:
    """
    Checks for changes in HTML content using hash comparison.
    """
    
    def __init__(self):
        pass
    
    def has_content_changed(self, new_html_content, previous_html_hash):
        """
        Checks if the HTML content has changed compared to a previous hash.
        
        Args:
            new_html_content (str): New HTML content
            previous_html_hash (str): Previous HTML hash
            
        Returns:
            bool: True if content has changed, False otherwise
        """
        if not previous_html_hash:
            # If there's no previous hash, consider it as changed
            return True
        
        # Compute hash of new content
        new_html_hash = compute_html_hash(new_html_content)
        
        # Compare hashes
        return new_html_hash != previous_html_hash
    
    def get_content_hash(self, html_content):
        """
        Gets the hash of HTML content.
        
        Args:
            html_content (str): HTML content
            
        Returns:
            str: Hash of the HTML content
        """
        return compute_html_hash(html_content)