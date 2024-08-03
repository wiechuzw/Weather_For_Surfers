""" 
data_loading.py:
1- This program takes weather data from "weather.visualcrossing.com" and collect it in "data_weather\visualcrossing.csv"
2- start next program: data_plot.py
3- data_plot.py processes the data's weather, performs the weather graph and sends it to send_email 
4- data_plot.py start send_email_2
"""

import datetime
import requests
import subprocess
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

subprocess.run(["python", "data_plot.py"])