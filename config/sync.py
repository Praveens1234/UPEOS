# Sync configuration loader

import os
import yaml
from .settings import get_settings

class SyncConfig:
    """
    Loads and manages synchronization settings.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self._sync_settings = self.settings.get('sync', {})
    
    @property
    def data_states(self):
        """
        Gets the data states configuration.
        """
        return self._sync_settings.get('data_states', {
            'open': 'OPEN',
            'closing': 'CLOSING',
            'closed': 'CLOSED'
        })
    
    @property
    def freshness_thresholds(self):
        """
        Gets the freshness thresholds configuration.
        """
        return self._sync_settings.get('freshness_thresholds', {
            'open': 1,      # 1 hour
            'closing': 24,  # 24 hours
            'closed': 168   # 168 hours (7 days)
        })
    
    @property
    def default_sync_mode(self):
        """
        Gets the default sync mode.
        """
        return self._sync_settings.get('default_sync_mode', 'missing_only')