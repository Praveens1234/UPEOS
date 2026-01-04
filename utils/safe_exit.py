# Graceful shutdown handlers

import signal
import sys
from ..db.connection import DatabaseConnection
from ..sync.engine import SyncEngine

# Global variables to track shutdown state
_shutdown_handlers = []
_is_shutting_down = False

def register_shutdown_handler(handler):
    """
    Registers a shutdown handler function to be called during graceful shutdown.
    
    Args:
        handler (callable): Function to be called during shutdown
    """
    _shutdown_handlers.append(handler)

def shutdown_handler(signum, frame):
    """
    Signal handler for graceful shutdown.
    """
    global _is_shutting_down
    
    if _is_shutting_down:
        # Already shutting down, ignore additional signals
        return
    
    _is_shutting_down = True
    print(f"Received signal {signum}, initiating graceful shutdown...")
    
    # Call all registered shutdown handlers
    for handler in _shutdown_handlers:
        try:
            handler()
        except Exception as e:
            print(f"Error in shutdown handler: {e}")
    
    # Close any remaining database connections
    # Note: In a more complex application, we might want to keep track of all
    # database connections and close them explicitly here
    
    print("Shutdown complete")
    sys.exit(0)

def setup_signal_handlers():
    """
    Sets up signal handlers for graceful shutdown.
    """
    signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown_handler)  # Termination signal

def cleanup_database_connections():
    """
    Cleans up database connections during shutdown.
    """
    # In this implementation, we don't need to do anything special
    # because the DatabaseConnection class handles closing connections
    # in its destructor. However, in a more complex application, we might
    # want to keep track of all connections and close them explicitly.
    pass

def cleanup_sync_engines():
    """
    Cleans up sync engines during shutdown.
    """
    # Similar to database connections, the SyncEngine class should handle
    # cleanup in its destructor. This function is here as a placeholder
    # in case we need to add explicit cleanup logic in the future.
    pass

# Register built-in cleanup handlers
register_shutdown_handler(cleanup_database_connections)
register_shutdown_handler(cleanup_sync_engines)