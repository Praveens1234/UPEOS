# get_system_manifest()

def get_system_manifest():
    """
    Returns a machine-readable description of the UPEOS system.
    """
    return {
        "name": "UPEOS - Uttar Pradesh E-Procurement Service",
        "version": "1.0.0",
        "description": "A read-only, lawful, government-aligned data intelligence and reporting system for Uttar Pradesh paddy procurement data.",
        "purpose": "To automatically collect, organize, analyze, search, aggregate, and present publicly disclosed procurement information published by the Government of Uttar Pradesh for paddy procurement.",
        "governing_principles": {
            "db_first_policy": "Internal database is always checked first before accessing government website",
            "government_website_respect": "Never bypass security, authentication, or rate limits",
            "deterministic_behavior": "Same operation twice must not corrupt data or change outcomes",
            "transparency": "Every significant action must be traceable through structured activity logs",
            "no_inference": "System never guesses or fabricates information not explicitly present"
        },
        "supported_scopes": [
            "centre",
            "selected",
            "all"
        ],
        "date_time_models": {
            "single": "Single date",
            "range": "Date range (inclusive)",
            "latest": "Latest available date",
            "all": "ALL historical data",
            "batch": "Batch discrete dates"
        },
        "tool_categories": {
            "discovery": [
                "list_centres",
                "list_centres_by_district",
                "get_system_status",
                "get_last_sync_status"
            ],
            "data_retrieval": [
                "get_centre_summary",
                "get_date_summary",
                "get_latest_summary",
                "get_global_summary"
            ],
            "statistics": [
                "get_stats",
                "get_stats_between_dates",
                "get_total_quantity",
                "get_total_amount",
                "get_total_farmers"
            ],
            "search": [
                "search_farmer",
                "search_by_village",
                "advanced_search",
                "batch_search"
            ],
            "aggregation": [
                "get_daily_breakdown",
                "get_centre_comparison",
                "get_top_centres_by_quantity",
                "get_top_centres_by_amount"
            ],
            "export": [
                "export_transactions_detailed",
                "export_daywise_statement",
                "export_and_upload_report",
                "list_generated_reports",
                "get_report_info"
            ],
            "sync": [
                "sync_latest",
                "sync_centre",
                "sync_date",
                "sync_between_dates",
                "rebuild_aggregates",
                "full_sync"
            ],
            "logs": [
                "get_activity_logs",
                "get_recent_errors",
                "get_sync_history",
                "validate_db_integrity"
            ]
        },
        "usage_guidelines": {
            "read_only_default": "All external requests are read-only by default",
            "explicit_sync": "Any operation that triggers website access (sync) must be explicit and controlled",
            "db_first_responses": "DB-first responses for flash speed",
            "transparent_logging": "All significant system actions must be traceable through structured activity logs",
            "rate_limiting": "Respects government website rate limits to ensure sustainable access",
            "data_integrity": "Maintains official data accuracy without inference or modification"
        },
        "known_limitations": {
            "environment_constraints": "Designed for Android Termux with proot-distro Ubuntu Linux",
            "no_browser_automation": "No browser automation, graphical interfaces, headless browsers, Playwright, Selenium, or JavaScript execution",
            "opaque_urls": "All website URLs and parameters are treated as opaque tokens",
            "link_based_navigation": "Navigation must be performed strictly by following hyperlinks as presented in HTML anchor tags",
            "no_parallel_scraping": "Sequential, respectful data collection to protect government infrastructure"
        },
        "features": {
            "data_collection": "Automated synchronization with Government of Uttar Pradesh procurement website",
            "data_storage": "Local SQLite database with efficient indexing and querying",
            "data_analysis": "Statistical aggregation and reporting capabilities",
            "data_search": "Advanced search and filtering of farmer transactions",
            "data_export": "Professional PDF report generation with cloud upload capability",
            "api_access": "RESTful API interface for programmatic access",
            "mcp_integration": "Model Context Protocol support for AI agent interaction",
            "logging": "Comprehensive activity logging and audit trails",
            "error_handling": "Robust error handling and recovery mechanisms"
        },
        "performance": {
            "db_first_policy": "Millisecond response times for cached data",
            "rate_limiting": "Configurable delays between requests (default 1 second)",
            "parallel_processing": "Multi-threaded sync engine for efficient data collection",
            "memory_efficient": "Streaming exports for large datasets",
            "indexed_queries": "Optimized database queries with proper indexing"
        }
    }