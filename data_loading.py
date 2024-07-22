"""
The code retrieves weather data from the Visual Crossing API and saves it to a JSON file.
The script performs the following steps:
1. Defines the URL to the Visual Crossing API with request parameters (location, metric units, API key, and response format).
2. Sets the output directory and filename for saving data.
3. Sends a request to the API and checks if the response is correct.
4. Creates the output directory if it does not exist.
5. Saves the response data in JSON format to a file.
6. Prints a message about saving the data along with the time of downloading the data.
"""

import datetime
import requests
import sys
import os

URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Polska%20Gocza%C5%82kowice%20Zdr%C3%B3j?unitGroup=metric&include=hours&key=ZGDXV9ZMHP5GK77U9ZFM7JXSE&contentType=csv'
OUTPUT_DIR = './data_weather'  
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, 'visualcrossing.csv')

response = requests.get(URL)
if not response.ok:
    print('Data download error')
    sys.exit(1)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
response.encoding = 'utf-8'

with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as file:
    file.write(response.text)

print(f'Data saved in {OUTPUT_FILENAME}; Time of data download -> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')