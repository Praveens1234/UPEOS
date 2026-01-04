# UPEOS - Uttar Pradesh E-Procurement Service

UPEOS is a read-only, lawful, government-aligned data intelligence and reporting system for Uttar Pradesh paddy procurement data.

## Overview

UPEOS automatically collects, organizes, analyzes, searches, aggregates, and presents publicly disclosed procurement information published by the Government of Uttar Pradesh for paddy procurement. The system operates with strict adherence to legal, ethical, and technical boundaries while improving accessibility, analysis, reporting, and transparency.

## Key Features

- **Data Collection**: Automated synchronization with Government of Uttar Pradesh procurement website
- **Data Storage**: Local SQLite database with efficient indexing and querying
- **Data Analysis**: Statistical aggregation and reporting capabilities
- **Data Search**: Advanced search and filtering of farmer transactions
- **Data Export**: Professional PDF report generation with cloud upload capability
- **API Access**: RESTful API interface for programmatic access
- **MCP Integration**: Model Context Protocol support for AI agent interaction
- **Logging**: Comprehensive activity logging and audit trails
- **Error Handling**: Robust error handling and recovery mechanisms

## System Architecture

UPEOS follows a layered, modular, DB-centric architecture:

1. **Request Ingress Layer** (API / MCP)
2. **Request Router and Decision Engine**
3. **Internal Database** (Primary Working Memory)
4. **Website Data Acquisition Layer**
5. **HTML Analysis and Extraction Layer**
6. **Normalization and Validation Layer**
7. **Aggregation and Statistics Layer**
8. **Sync Engine** (Automatic and Manual)
9. **Activity Logs Manager**
10. **Protection, Recovery, and Safety Systems**

## Technology Stack

- **Language**: Python 3.x
- **Web Framework**: FastAPI with Uvicorn
- **Database**: SQLite
- **HTML Parsing**: BeautifulSoup4 with lxml
- **HTTP Client**: requests
- **PDF Generation**: reportlab
- **Configuration**: PyYAML
- **Environment**: Android Termux with proot-distro Ubuntu Linux

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd upeos

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Configuration

Configuration files are located in the `config/` directory:

- `settings.yaml`: Global configuration settings
- `logging.yaml`: Logging configuration
- `sync.yaml`: Synchronization behavior and freshness rules

## API Documentation

See [API Documentation](docs/API_DOCUMENTATION.md) for detailed API reference.

Base URL: `http://localhost:8001/api/v1`

### Quick API Examples

```bash
# List all centres
curl -X GET "http://localhost:8001/api/v1/centres"

# Get centre summary
curl -X GET "http://localhost:8001/api/v1/centres/{centre_name}/summary"

# Search farmers
curl -X GET "http://localhost:8001/api/v1/search/farmer?farmer_name=SHRI"

# Export report
curl -X GET "http://localhost:8001/api/v1/export/summary/daywise?centre_id=1&upload=true"
```

## MCP Documentation

See [MCP Documentation](docs/MCP_DOCUMENTATION.md) for detailed MCP reference.

### Quick MCP Examples

```python
# Get system manifest
manifest = mcp.call_tool("get_system_manifest")

# List all centres
centres = mcp.call_tool("list_centres")

# Export report
report = mcp.call_tool("export_transactions_detailed", {
    "centre_id": 1,
    "date": "02/01/2026",
    "upload": True
})
```

## Data Model

### Centres
Represents procurement centres with name and URL information.

### Date-wise Summaries
Contains official farmer counts, quantities, and amounts for each date at each centre.

### Farmer Transactions
Stores detailed transaction information for individual farmers including ID, name, village, quantity, amount, and transaction time.

## Synchronization

UPEOS supports both automatic and manual synchronization:

- **Automatic**: Background sync on system startup
- **Manual**: API/MCP calls to trigger sync operations
- **Selective**: Sync specific centres or date ranges
- **Full**: Complete data synchronization

## PDF Reports

UPEOS generates professional PDF reports with:

- Modern, clean design
- Proper formatting of rupee symbols (₹)
- Summary statistics
- Detailed transaction tables
- Headers, footers, and page numbering
- Cloud upload capability (Catbox.moe)

## Governance Principles

1. **DB-First Policy**: Internal database is always checked first before accessing government website
2. **Government Website Respect**: Never bypass security, authentication, or rate limits
3. **Deterministic Behavior**: Same operation twice must not corrupt data or change outcomes
4. **Transparency**: Every significant action must be traceable through structured activity logs
5. **No Inference**: System never guesses or fabricates information not explicitly present

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Government of Uttar Pradesh for publishing procurement data
- Open source community for the tools and libraries used
- Developers and contributors who have helped build this system

## Support

For support, please open an issue on the repository or contact the maintainers.