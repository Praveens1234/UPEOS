# SHA/hash utilities

import hashlib

def compute_html_hash(html_content):
    """
    Computes a SHA-256 hash of HTML content.
    
    Args:
        html_content (str): HTML content to hash
        
    Returns:
        str: SHA-256 hash of the HTML content
    """
    if not html_content:
        return None
    
    # Encode the HTML content to bytes
    content_bytes = html_content.encode('utf-8')
    
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the content bytes
    sha256_hash.update(content_bytes)
    
    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()

def compute_file_hash(file_path):
    """
    Computes a SHA-256 hash of a file.
    
    Args:
        file_path (str): Path to the file to hash
        
    Returns:
        str: SHA-256 hash of the file content
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(file_path, "rb") as f:
            # Read the file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return None