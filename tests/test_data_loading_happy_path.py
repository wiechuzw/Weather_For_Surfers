"""
Tests of the `download_weather_data` function from the `data_loading` module.

The test class contains tests that check the correct operation of the `load_weather_data` function and error handling.
The tests are run in a temporary test directory.

Test methods:

- `test_happy_path`:
Tests the correct operation of the `load_weather_data` function under normal conditions.
Simulates successful data download and writing to a file. Verifies that
the file was opened in write mode and that the data was saved correctly.

- `test_program_exit_on_error`:
Tests whether the program exits correctly with error code 1,
when an error occurs while downloading data. Simulates a `RequestException`
exception during data download and checks whether the `sys.exit(1)` function was called.
"""
import os
import shutil
import tempfile
import unittest

from unittest.mock import patch, mock_open, MagicMock

import requests

import data_loading


class TestDataLoading(unittest.TestCase):

    def setUp(self):
        """Creating a temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.original_output_dir = data_loading.OUTPUT_DIR
        data_loading.OUTPUT_DIR = self.test_dir
        data_loading.OUTPUT_FILENAME = os.path.join(self.test_dir, 'visualcrossing.csv')

    def tearDown(self):
        """Deleting the temporary test directory after testing is complete"""
        shutil.rmtree(self.test_dir)
        data_loading.OUTPUT_DIR = self.original_output_dir
        data_loading.OUTPUT_FILENAME = os.path.join(self.original_output_dir, 'visualcrossing.csv')

    @patch('data_loading.requests.get')
    @patch('data_loading.open', new_callable=mock_open)
    def test_happy_path(self, mock_file, mock_get):
        """Testing the correct operation of the script"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "test_csv_content"
        mock_get.return_value = mock_response

        """Starting the function"""
        data_loading.download_weather_data()

        """Checking if the file was opened in write mode"""
        mock_file.assert_any_call(data_loading.OUTPUT_FILENAME, 'w', encoding='utf-8')
        
        """Checking if data has been written to the file"""
        mock_file().write.assert_called_with("test_csv_content")

    @patch('data_loading.sys.exit')
    @patch('data_loading.requests.get', side_effect=requests.RequestException("Error"))
    def test_program_exit_on_error(self, mock_get, mock_exit):
        """Test of program termination in case of error"""
        data_loading.download_weather_data()
        
        """Checking if the program exited with code 1"""
        mock_exit.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
