# Settings loader

import os
import yaml

class Settings:
    """
    Loads and manages application settings from YAML files.
    """
    
    # Default settings
    _defaults = {
        'request_delay': 1.0,
        'database_path': './data/upeos.db',
        'log_directory': './logs',
        'report_directory': './reports',
        'creport_registry': './data/creports.json',
        'enable_cloud_upload': True,  # Changed default to True
        'max_retries': 3
    }
    
    def __init__(self, config_dir="./config"):
        self.config_dir = config_dir
        self._settings = self._defaults.copy()
        self._load_settings()
    
    def _load_settings(self):
        """
        Loads settings from YAML files.
        """
        # Load main settings
        settings_file = os.path.join(self.config_dir, "settings.yaml")
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                loaded_settings = yaml.safe_load(f) or {}
                self._settings.update(loaded_settings)
        
        # Load logging settings
        logging_file = os.path.join(self.config_dir, "logging.yaml")
        if os.path.exists(logging_file):
            with open(logging_file, 'r') as f:
                logging_settings = yaml.safe_load(f)
                if logging_settings:
                    self._settings['logging'] = logging_settings
        
        # Load sync settings
        sync_file = os.path.join(self.config_dir, "sync.yaml")
        if os.path.exists(sync_file):
            with open(sync_file, 'r') as f:
                sync_settings = yaml.safe_load(f)
                if sync_settings:
                    self._settings['sync'] = sync_settings
    
    def get(self, key, default=None):
        """
        Gets a setting value by key.
        
        Args:
            key (str): Setting key
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        return self._settings.get(key, default)
    
    def __getattr__(self, name):
        """
        Allows accessing settings as attributes.
        """
        return self._settings.get(name, None)
    
    def __getitem__(self, key):
        """
        Allows accessing settings as dictionary items.
        """
        return self._settings.get(key)

# Global settings instance
_settings_instance = None

def get_settings():
    """
    Gets the global settings instance.
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance