# Date+time state (open/closing/closed)

from datetime import datetime, timedelta
from ..db.repositories.summary_repo import SummaryRepository
from ..config.sync import SyncConfig

class FreshnessManager:
    """
    Manages data freshness states (OPEN, CLOSING, CLOSED) for synchronization.
    """
    
    def __init__(self, db_connection):
        self.summary_repo = SummaryRepository(db_connection)
        self.sync_config = SyncConfig()
    
    def determine_data_state(self, date):
        """
        Determines the data state (OPEN, CLOSING, CLOSED) for a given date.
        
        Args:
            date (str): Date in DD/MM/YYYY format
            
        Returns:
            str: Data state (OPEN, CLOSING, or CLOSED)
        """
        # Convert string date to datetime object
        try:
            date_obj = datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            print(f"Warning: Invalid date format: {date}")
            return 'OPEN'  # Default to OPEN if date is invalid
        
        # Get current date
        current_date = datetime.now()
        
        # Calculate days difference
        days_diff = (current_date - date_obj).days
        
        # Determine state based on age of data
        if days_diff < 1:
            # Today or future dates are considered OPEN
            return 'OPEN'
        elif days_diff < 7:
            # Recent past (1-7 days) is considered CLOSING
            return 'CLOSING'
        else:
            # Older data (more than 7 days) is considered CLOSED
            return 'CLOSED'
    
    def is_data_fresh(self, centre_id, date):
        """
        Checks if data for a specific centre and date is fresh.
        
        Args:
            centre_id (int): Centre ID
            date (str): Date in DD/MM/YYYY format
            
        Returns:
            bool: True if data is fresh, False otherwise
        """
        # Get the summary from database
        summary = self.summary_repo.get_summary_by_centre_and_date(centre_id, date)
        if not summary:
            return False  # No data means not fresh
        
        # Determine expected freshness based on data state
        data_state = self.determine_data_state(date)
        thresholds = self.sync_config.freshness_thresholds
        threshold_hours = thresholds.get(data_state, thresholds['open'])
        
        # Calculate time since last sync
        last_synced = datetime.strptime(summary['last_synced'], '%Y-%m-%d %H:%M:%S')
        current_time = datetime.now()
        hours_since_sync = (current_time - last_synced).total_seconds() / 3600
        
        # Check if data is fresh
        return hours_since_sync < threshold_hours
    
    def update_data_state(self, centre_id, date):
        """
        Updates the data state for a specific centre and date.
        
        Args:
            centre_id (int): Centre ID
            date (str): Date in DD/MM/YYYY format
            
        Returns:
            str: Updated data state
        """
        data_state = self.determine_data_state(date)
        
        # Here we would normally update the database with the new state
        # For now, we'll just return the determined state
        return data_state