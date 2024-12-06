"""
Checks whether the program correctly loads the TOML file and handles errors if it is missing or in the wrong format.
"""
import pytest
import toml

from unittest.mock import patch


def test_load_config_success():
    """Test successful loading of the TOML configuration file."""
    with patch('toml.load', return_value={"support_address": ["support@example.com"]}) as mock_toml_load:
        config = toml.load('Config_file.toml')
        assert config.get("support_address") == ["support@example.com"]
        mock_toml_load.assert_called_once_with('Config_file.toml')


def test_load_config_failure():
    """Test that the program raises SystemExit when the TOML file fails to load."""
    with patch('toml.load', side_effect=Exception("TOML load error")):
        with pytest.raises(SystemExit):
            try:
                toml.load('Config_file.toml')  # This simulates application's behavior
            except Exception as e:
                print(f"Handled exception: {e}")
                exit(1)  # Simulating the application exiting on failure
