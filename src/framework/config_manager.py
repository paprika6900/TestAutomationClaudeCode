"""
Configuration manager for loading and accessing test framework settings.
"""
import os
import yaml
from pathlib import Path


class ConfigManager:
    """Manages configuration settings for the test framework."""

    _instance = None
    _config = None

    def __new__(cls):
        """Singleton pattern to ensure only one config instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the config manager and load configuration."""
        if self._config is None:
            self.load_config()

    def load_config(self, config_path: str = None):
        """
        Load configuration from YAML file.

        Args:
            config_path: Path to config file. If None, uses default config.yaml
        """
        if config_path is None:
            # Get project root directory
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config.yaml"

        with open(config_path, 'r') as file:
            self._config = yaml.safe_load(file)

    def get(self, key_path: str, default=None):
        """
        Get configuration value using dot notation.

        Args:
            key_path: Configuration key in dot notation (e.g., 'browser.name')
            default: Default value if key not found

        Returns:
            Configuration value or default

        Example:
            config.get('browser.name')  # Returns 'chrome'
            config.get('browser.headless')  # Returns False
        """
        keys = key_path.split('.')
        value = self._config

        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_browser_config(self) -> dict:
        """Get all browser configuration settings."""
        return self._config.get('browser', {})

    def get_selenium_config(self) -> dict:
        """Get all selenium configuration settings."""
        return self._config.get('selenium', {})

    def get_test_data_config(self) -> dict:
        """Get all test data configuration settings."""
        return self._config.get('test_data', {})

    @property
    def config(self) -> dict:
        """Get the full configuration dictionary."""
        return self._config


# Global config instance
config = ConfigManager()
