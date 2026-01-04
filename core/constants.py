# System Constants and Rules

# Government Website URLs (treated as opaque tokens)
BASE_URL = "https://eproc.up.gov.in/Paddy2324/Uparjan/Mukhyalay/PaddyPurchaseSummary/PurchaseReport_Center.aspx?Dcode=SFFfMTcyX0hRMThfTlRfMV8xXzE0IzIwMjUtMjAyNiMx"

# Data States
DATA_STATE_OPEN = "OPEN"
DATA_STATE_CLOSING = "CLOSING"
DATA_STATE_CLOSED = "CLOSED"

# Date Format
DATE_FORMAT = "%d/%m/%Y"

# System Rules
SYSTEM_RULES = {
    "db_first": True,
    "never_guess": True,
    "opaque_urls": True,
    "follow_links_only": True,
    "no_direct_url_construction": True,
    "no_javascript": True,
    "no_browser_automation": True,
    "respect_rate_limits": True,
    "deterministic_behavior": True,
    "transparent_logging": True
}