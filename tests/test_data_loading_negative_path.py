"""
Negative tests for the `load_weather_data` function in the `data_loading` module.

These tests check how the function handles various types of errors,
that can occur during data retrieval, file saving, and directory creation.

Test methods:

- `test_error_during_directory_creation`:
Simulates an error during directory creation by setting `self.mock_makedirs.side_effect` to raise `OSError`.
Additionally, sets `self.mock_exists.return_value` to `False` to ensure that `os.makedirs` was called.
Calls `load_weather_data()` and checks if `sys.exit(1)` was called.

- `test_error_during_data_saving`:
Simulates a file saving error by setting `self.mock_open.side_effect` to raise `IOError`.
Calls `load_weather_data()` and checks if `sys.exit(1)` was called.

- `test_error_during_data_retrieval`:
Simulates a network error by setting `self.mock_get.side_effect` to raise `RequestException`.
Calls the `load_weather_data()` function and checks if `sys.exit(1)` was called, indicating that the program exited due to an error.
"""
import os
import shutil
import tempfile
import unittest

from unittest.mock import patch

import data_loading

import requests


class TestDataLoadingNegativePath(unittest.TestCase):

    def setUp(self):
        """Creating a temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.original_output_dir = data_loading.OUTPUT_DIR
        data_loading.OUTPUT_DIR = self.test_dir
        data_loading.OUTPUT_FILENAME = os.path.join(self.test_dir, 'visualcrossing.csv')

        """Patch sys.exit to prevent the test from actually calling sys.exit"""
        self.patcher_exit = patch('sys.exit')
        self.mock_exit = self.patcher_exit.start()
        
        """Patch os.makedirs to control its behavior in tests"""
        self.patcher_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patcher_makedirs.start()

        """Patch requests.get to control its behavior in tests"""
        self.patcher_get = patch('requests.get')
        self.mock_get = self.patcher_get.start()

    def tearDown(self):
        """Deleting the temporary test directory after testing is complete"""
        shutil.rmtree(self.test_dir)
        data_loading.OUTPUT_DIR = self.original_output_dir
        data_loading.OUTPUT_FILENAME = os.path.join(self.original_output_dir, 'visualcrossing.csv')

        """Stop all patches"""
        self.patcher_exit.stop()
        self.patcher_makedirs.stop()
        self.patcher_get.stop()

    @patch('os.makedirs', side_effect=Exception("Directory creation error"))
    def test_error_during_directory_creation(self, mock_makedirs):
        """Test if sys.exit is called when directory creation fails"""
        data_loading.load_weather_data()
        self.mock_exit.assert_called_with(1)

    @patch('builtins.open', side_effect=Exception("File write error"))
    def test_error_during_data_saving(self, mock_open):
        """Test if sys.exit is called when file write fails"""
        data_loading.load_weather_data()
        self.mock_exit.assert_called_with(1)

    @patch('requests.get', side_effect=requests.RequestException("Network Error"))
    def test_error_during_data_retrieval(self, mock_get):
        """Test if sys.exit is called when the data retrieval fails"""
        data_loading.load_weather_data()
        self.mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()


