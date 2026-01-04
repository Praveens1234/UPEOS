# MCP server bootstrap

import json
from ..mcp.manifest import get_system_manifest
from ..mcp.tools.discovery import list_centres, list_centres_by_district
from ..mcp.tools.data import get_centre_summary, get_date_summary, get_latest_summary
from ..mcp.tools.stats import get_stats, get_total_quantity, get_total_amount, get_total_farmers
from ..mcp.tools.search import search_farmer, search_by_village, advanced_search
from ..mcp.tools.export import export_transactions_detailed, export_daywise_statement, list_generated_reports, get_report_info
from ..mcp.tools.sync import sync_all_centres, sync_centre, sync_centre_date
from ..mcp.tools.logs import get_activity_logs, get_recent_errors

# Define the available MCP tools
MCP_TOOLS = {
    # Discovery tools
    "list_centres": list_centres,
    "list_centres_by_district": list_centres_by_district,
    
    # Data retrieval tools
    "get_centre_summary": get_centre_summary,
    "get_date_summary": get_date_summary,
    "get_latest_summary": get_latest_summary,
    
    # Statistics tools
    "get_stats": get_stats,
    "get_total_quantity": get_total_quantity,
    "get_total_amount": get_total_amount,
    "get_total_farmers": get_total_farmers,
    
    # Search tools
    "search_farmer": search_farmer,
    "search_by_village": search_by_village,
    "advanced_search": advanced_search,
    
    # Export tools
    "export_transactions_detailed": export_transactions_detailed,
    "export_daywise_statement": export_daywise_statement,
    "list_generated_reports": list_generated_reports,
    "get_report_info": get_report_info,
    
    # Sync tools
    "sync_all_centres": sync_all_centres,
    "sync_centre": sync_centre,
    "sync_centre_date": sync_centre_date,
    
    # Logs tools
    "get_activity_logs": get_activity_logs,
    "get_recent_errors": get_recent_errors,
}

def handle_mcp_request(request):
    """
    Handles an MCP request and returns the appropriate response.
    
    Args:
        request (dict): The MCP request
        
    Returns:
        dict: The MCP response
    """
    # Handle system manifest request
    if request.get("method") == "get_system_manifest":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": get_system_manifest()
        }
    
    # Handle tool calls
    if request.get("method") == "call_tool":
        tool_name = request.get("params", {}).get("name")
        tool_args = request.get("params", {}).get("arguments", {})
        
        if tool_name in MCP_TOOLS:
            try:
                result = MCP_TOOLS[tool_name](**tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32000,
                        "message": f"Tool execution failed: {str(e)}"
                    }
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {tool_name}"
                }
            }
    
    # Handle unknown methods
    return {
        "jsonrpc": "2.0",
        "id": request.get("id"),
        "error": {
            "code": -32601,
            "message": f"Method not found: {request.get('method')}"
        }
    }