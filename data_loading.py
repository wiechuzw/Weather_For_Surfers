"""
data_loading.py: loads weather data from a specified URL and stores it in "data_weather\visualcrossing.csv"; it handles errors both during data retrieval and during data saving by printing error messages and terminating the program on errors.
"""

import datetime
import requests
import sys
import os

URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Polska%20Gocza%C5%82kowice%20Zdr%C3%B3j?unitGroup=metric&include=hours&key=ZGDXV9ZMHP5GK77U9ZFM7JXSE&contentType=csv'
OUTPUT_DIR = './data_weather'
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'visualcrossing.csv')

try:
    response = requests.get(URL)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"Data download error: {e}")
    sys.exit(1)

try:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    response.encoding = 'utf-8'

    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as file:
        file.write(response.text)

    print(f'Data saved in {OUTPUT_FILENAME}; Time of data download -> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
except Exception as e:
    print(f"An error occurred while saving data: {e}")
    sys.exit(1)