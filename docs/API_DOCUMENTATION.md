# UPEOS API Documentation

## Overview

UPEOS (Uttar Pradesh E-Procurement Service) provides a RESTful API for accessing and analyzing Uttar Pradesh paddy procurement data. The API follows standard REST conventions and returns JSON responses.

## Base URL

```
http://localhost:8001/api/v1
```

## Authentication

The API does not require authentication for read operations. All data is publicly available from the Government of Uttar Pradesh procurement website.

## Rate Limiting

The API respects rate limits when accessing the government website:
- Minimum 1 second delay between requests to the same domain
- Configurable in `/config/settings.yaml`

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message"
}
```

## API Endpoints

### Discovery

#### List All Centres
```
GET /centres
```

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

#### Get Centre by Name
```
GET /centres/{centre_name}
```

Returns details of a specific centre.

**Parameters:**
- `centre_name` (path): Name of the centre (URL encoded)

**Response:**
```json
{
  "centre": {
    "id": 1,
    "name": "UPSSखागा मंडी - खागा नगर पंचायत",
    "url": "https://eproc.up.gov.in/...",
    "district": null
  }
}
```

#### List Centres by District
```
GET /districts/{district_name}/centres
```

Returns centres in a specific district.

**Parameters:**
- `district_name` (path): Name of the district (URL encoded)

### Data Retrieval

#### Get Centre Summary
```
GET /centres/{centre_name}/summary
```

Returns all date-wise summaries for a centre.

#### Get Latest Summary
```
GET /centres/{centre_name}/summary/latest
```

Returns the latest date-wise summary for a centre.

#### Get Date Summary
```
GET /centres/{centre_name}/summary/{date}
```

Returns the summary for a specific date at a centre.

**Parameters:**
- `date`: Date in DD/MM/YYYY format

### Statistics

#### Get Statistics
```
GET /stats
```

Returns comprehensive statistics.

**Query Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `date` (optional): Specific date in DD/MM/YYYY format

#### Get Total Quantity
```
GET /stats/total-quantity
```

Returns total quantity aggregated by centre and/or date range.

**Query Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### Get Total Amount
```
GET /stats/total-amount
```

Returns total amount aggregated by centre and/or date range.

#### Get Total Farmers
```
GET /stats/total-farmers
```

Returns total farmer count aggregated by centre and/or date range.

#### Get Daily Breakdown
```
GET /stats/daily-breakdown
```

Returns date-wise breakdown of procurement data.

#### Get Centre Comparison
```
GET /stats/centre-comparison
```

Returns centre-wise comparison of procurement data.

### Search

#### Search Farmers
```
GET /search/farmer
```

Searches for farmer transactions based on various criteria.

**Query Parameters:**
- `farmer_name` (required): Farmer name or partial name to search for
- `village` (optional): Village name or partial name to filter by
- `min_quantity` (optional): Minimum quantity filter
- `max_quantity` (optional): Maximum quantity filter
- `min_amount` (optional): Minimum amount filter
- `max_amount` (optional): Maximum amount filter
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### Search by Village
```
GET /search/village
```

Searches for villages matching the given criteria.

**Query Parameters:**
- `village` (required): Village name or partial name to search for
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format

#### Advanced Search
```
GET /search/advanced
```

Performs an advanced search with multiple criteria.

### Export

#### Export Detailed Transactions
```
GET /export/transactions/detailed
```

Exports detailed farmer transaction data to PDF.

**Query Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `date` (optional): Specific date in DD/MM/YYYY format
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format
- `upload` (optional): Whether to upload the report to cloud storage (boolean)

#### Export Day-wise Statement
```
GET /export/summary/daywise
```

Exports day-wise summary data to PDF.

**Query Parameters:**
- `centre_id` (optional): Centre ID to filter by
- `from_date` (optional): Start date in DD/MM/YYYY format
- `to_date` (optional): End date in DD/MM/YYYY format
- `upload` (optional): Whether to upload the report to cloud storage (boolean)

#### List Generated Reports
```
GET /export/reports
```

Lists all generated reports.

#### Get Report Info
```
GET /export/reports/{file_path}
```

Gets information about a specific report.

### Synchronization

#### Sync All Centres
```
POST /sync/all-centres
```

Synchronizes all centres from the government website.

#### Sync Centre
```
POST /sync/centre/{centre_name}
```

Synchronizes date-wise data for a specific centre.

#### Sync Centre Date
```
POST /sync/centre/{centre_name}/date/{date}
```

Synchronizes farmer details for a specific centre and date.

### Logs

#### Get Activity Logs
```
GET /logs
```

Retrieves activity logs with optional filtering.

**Query Parameters:**
- `component` (optional): Component to filter by
- `level` (optional): Log level to filter by (INFO, WARNING, ERROR)
- `limit` (optional): Maximum number of logs to return (default: 100)

#### Get Recent Errors
```
GET /logs/errors
```

Retrieves recent error logs.

**Query Parameters:**
- `limit` (optional): Maximum number of error logs to return (default: 10)

## Examples

### Get All Centres
```bash
curl -X GET "http://localhost:8001/api/v1/centres"
```

### Get Centre Summary
```bash
curl -X GET "http://localhost:8001/api/v1/centres/UPSS%E0%A4%96%E0%A4%BE%E0%A4%97%E0%A4%BE%20%E0%A4%AE%E0%A4%82%E0%A4%A1%E0%A5%80%20-%20%E0%A4%96%E0%A4%BE%E0%A4%97%E0%A4%BE%20%E0%A4%A8%E0%A4%97%E0%A4%B0%20%E0%A4%AA%E0%A4%82%E0%A4%9A%E0%A4%BE%E0%A4%AF%E0%A4%A4/summary"
```

### Get Total Quantity
```bash
curl -X GET "http://localhost:8001/api/v1/stats/total-quantity"
```

### Search Farmers
```bash
curl -X GET "http://localhost:8001/api/v1/search/farmer?farmer_name=SHRI"
```

### Export Day-wise Summary
```bash
curl -X GET "http://localhost:8001/api/v1/export/summary/daywise?centre_id=1&upload=true"
```

## Response Codes

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Data Models

### Centre
```json
{
  "id": 1,
  "name": "string",
  "url": "string",
  "district": "string or null"
}
```

### Date-wise Summary
```json
{
  "id": 1,
  "centre_id": 1,
  "date": "DD/MM/YYYY",
  "farmer_count": 0,
  "quantity": 0.0,
  "amount": 0.0,
  "details_url": "string",
  "data_state": "OPEN|CLOSING|CLOSED",
  "html_hash": "string"
}
```

### Farmer Transaction
```json
{
  "id": 1,
  "centre_id": 1,
  "date": "DD/MM/YYYY",
  "farmer_id": "string",
  "farmer_name": "string",
  "village": "string",
  "quantity": 0.0,
  "amount": 0.0,
  "transaction_time": "string"
}
```