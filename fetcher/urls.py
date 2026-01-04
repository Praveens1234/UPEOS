# Entry-point URLs only (no constructed URLs)

from ..core.constants import BASE_URL

# Base URL for the procurement system
PROCUREMENT_BASE_URL = BASE_URL

# Dictionary to store discovered URLs during runtime
DISCOVERED_URLS = {
    'centre_list': PROCUREMENT_BASE_URL,
    'centre_datewise_template': None,  # Will be discovered during runtime
    'farmer_details_template': None    # Will be discovered during runtime
}