# UPEOS MCP Documentation

## Overview

UPEOS (Uttar Pradesh E-Procurement Service) supports the Model Context Protocol (MCP) for AI agent interaction. This documentation describes the available MCP tools and how to use them.

## Getting Started

To interact with UPEOS via MCP, connect to the MCP server and call the `get_system_manifest()` tool first to understand the system capabilities.

## System Manifest

Call `get_system_manifest()` to get a complete description of the UPEOS system:

```json
{
  "name": "UPEOS - Uttar Pradesh E-Procurement Service",
  "version": "1.0.0",
  "description": "A read-only, lawful, government-aligned data intelligence and reporting system for Uttar Pradesh paddy procurement data.",
  "purpose": "To automatically collect, organize, analyze, search, aggregate, and present publicly disclosed procurement information published by the Government of Uttar Pradesh for paddy procurement.",
  // ... other manifest details
}
```

## Available Tools

### Discovery Tools

#### `list_centres()`
Returns a list of all procurement centres.

**Response:**
```json
{
  "centres": [
    {
      "id": 1,
      "name": "UPSSखागा मंडी - खागा नगर पंचायत",
      "url": "https://eproc.up.gov.in/...",
      "district": null
    }
  ]
}
```

#### `list_centres_by_district(district_name: str)`
Returns centres in a specific district.

**Parameters:**
- `district_name`: Name of the district

#### `get_system_status()`
Returns the current system status.

#### `get_last_sync_status()`
Returns the status of the last synchronization.

### Data Retrieval Tools

#### `get_centre_summary(centre_name: str)`
Returns all date-wise summaries for a centre.

**Parameters:**
- `centre_name`: Name of the centre

#### `get_date_summary(centre_name: str, date: str)`
Returns the summary for a specific date at a centre.

**Parameters:**
- `centre_name`: Name of the centre
- `date`: Date in DD/MM/YYYY format

#### `get_latest_summary(centre_name: str)`
Returns the latest date-wise summary for a centre.

**Parameters:**
- `centre_name`: Name of the centre

#### `get_global_summary()`
Returns global summary data across all centres.

### Statistics Tools

#### `get_stats(centre_id: int = None, date: str = None)`
Returns comprehensive statistics.

**Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `date` (optional): Specific date in DD/MM/YYYY format

#### `get_total_quantity(centre_id: int = None, from_date: str = None, to_date: str = None)`
Returns total quantity aggregated by centre and/or date range.

**Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### `get_total_amount(centre_id: int = None, from_date: str = None, to_date: str = None)`
Returns total amount aggregated by centre and/or date range.

#### `get_total_farmers(centre_id: int = None, from_date: str = None, to_date: str = None)`
Returns total farmer count aggregated by centre and/or date range.

### Search Tools

#### `search_farmer(farmer_name: str, village: str = None, min_quantity: float = None, max_quantity: float = None, min_amount: float = None, max_amount: float = None, from_date: str = None, to_date: str = None)`
Searches for farmer transactions based on various criteria.

**Parameters:**
- `farmer_name`: Farmer name or partial name to search for
- `village` (optional): Village name or partial name to filter by
- `min_quantity` (optional): Minimum quantity filter
- `max_quantity` (optional): Maximum quantity filter
- `min_amount` (optional): Minimum amount filter
- `max_amount` (optional): Maximum amount filter
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### `search_by_village(village: str, from_date: str = None, to_date: str = None)`
Searches for villages matching the given criteria.

**Parameters:**
- `village`: Village name or partial name to search for
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### `advanced_search(farmer_name: str = None, village: str = None, min_quantity: float = None, max_quantity: float = None, min_amount: float = None, max_amount: float = None, from_date: str = None, to_date: str = None)`
Performs an advanced search with multiple criteria.

### Aggregation Tools

#### `get_daily_breakdown(centre_id: int = None, from_date: str = None, to_date: str = None)`
Returns date-wise breakdown of procurement data.

#### `get_centre_comparison(date: str = None, from_date: str = None, to_date: str = None)`
Returns centre-wise comparison of procurement data.

#### `get_top_centres_by_quantity(limit: int = 10, from_date: str = None, to_date: str = None)`
Returns the top centres by total quantity procured.

#### `get_top_centres_by_amount(limit: int = 10, from_date: str = None, to_date: str = None)`
Returns the top centres by total amount paid.

### Export Tools

#### `export_transactions_detailed(centre_id: int = None, date: str = None, from_date: str = None, to_date: str = None, upload: bool = False)`
Exports detailed farmer transaction data to PDF.

**Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `date` (optional): Specific date in DD/MM/YYYY format
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format
- `upload` (optional): Whether to upload the report to cloud storage

#### `export_daywise_statement(centre_id: int = None, from_date: str = None, to_date: str = None, upload: bool = False)`
Exports day-wise summary data to PDF.

#### `export_and_upload_report(report_type: str, parameters: dict)`
Exports a report and uploads it to cloud storage.

#### `list_generated_reports()`
Lists all generated reports.

#### `get_report_info(file_path: str)`
Gets information about a specific report.

### Sync Tools

#### `sync_latest()`
Synchronizes the latest data from the government website.

#### `sync_centre(centre_name: str)`
Synchronizes date-wise data for a specific centre.

**Parameters:**
- `centre_name`: Name of the centre

#### `sync_date(centre_name: str, date: str)`
Synchronizes farmer details for a specific centre and date.

**Parameters:**
- `centre_name`: Name of the centre
- `date`: Date in DD/MM/YYYY format

#### `sync_between_dates(centre_name: str, from_date: str, to_date: str)`
Synchronizes data for a centre between two dates.

#### `rebuild_aggregates()`
Rebuilds pre-aggregated statistics.

#### `full_sync()`
Performs a full synchronization of all data.

### Logs Tools

#### `get_activity_logs(component: str = None, level: str = None, limit: int = 100)`
Retrieves activity logs with optional filtering.

#### `get_recent_errors(limit: int = 10)`
Retrieves recent error logs.

#### `get_sync_history(limit: int = 50)`
Retrieves synchronization history.

#### `validate_db_integrity()`
Validates database integrity.

## Usage Examples

### Python Example
```python
# Connect to MCP server
# Call get_system_manifest() first
manifest = mcp.call_tool("get_system_manifest")

# List all centres
centres = mcp.call_tool("list_centres")

# Get statistics for a specific centre
stats = mcp.call_tool("get_stats", {"centre_id": 1})

# Search for farmers
farmers = mcp.call_tool("search_farmer", {"farmer_name": "SHRI"})

# Export a detailed transaction report
report = mcp.call_tool("export_transactions_detailed", {
    "centre_id": 1,
    "date": "02/01/2026",
    "upload": True
})
```

### JSON-RPC Example
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "call_tool",
  "params": {
    "name": "list_centres",
    "arguments": {}
  }
}
```

## Best Practices

1. **Always call `get_system_manifest()` first** to understand available tools and system capabilities.

2. **Use DB-first policy**: The system prioritizes database queries over website access for speed and efficiency.

3. **Handle rate limiting**: Respect the system's rate limiting to avoid overwhelming the government website.

4. **Check data freshness**: Use sync tools when you need the most current data.

5. **Use appropriate scopes**: Filter data by centre or date range when possible to improve performance.

6. **Validate responses**: Always check response status and handle errors appropriately.

## Error Handling

All tools return structured responses. Errors will be in this format:

```json
{
  "error": "Error message"
}
```

Or for successful operations with warnings:

```json
{
  "status": "partial_success",
  "message": "Operation completed with warnings",
  "warnings": ["Warning message 1", "Warning message 2"]
}
```

## Security Considerations

- The system is read-only and does not modify government data
- All website interactions respect rate limits and security measures
- No authentication is required for legitimate use
- Data is sourced directly from official government publications

## Performance Guidelines

- Use specific filters rather than requesting all data
- Leverage the DB-first policy for faster responses
- Batch related requests when possible
- Avoid frequent sync operations unless necessary
- Use exported reports for large datasets rather than API queries

## Data Accuracy

- All data is sourced directly from the Government of Uttar Pradesh website
- The system maintains official farmer counts without inference
- Quantities and amounts are preserved exactly as published
- Historical data is maintained for analysis and reporting