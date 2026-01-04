# System entry point

import uvicorn
from upeos.api.app import app
from upeos.utils.safe_exit import setup_signal_handlers
from upeos.db.connection import DatabaseConnection
from upeos.db.migrations import DatabaseMigration

def initialize_database():
    """
    Initializes the database and applies any necessary migrations.
    """
    print("Initializing database...")
    db = DatabaseConnection()
    migration = DatabaseMigration(db)
    migration.migrate_to_latest()
    db.close()
    print("Database initialization complete")

def main():
    """
    Main entry point for the UPEOS application.
    """
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers()
    
    # Initialize database
    initialize_database()
    
    # Start the API server
    print("Starting UPEOS API server...")
    uvicorn.run(
        "upeos.api.app:app",
        host="127.0.0.1",
        port=8001,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()