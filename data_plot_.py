from typing import Any
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from sunrise_sunset import get_daylight_hours
import numpy as np
import seaborn as sns
import pandas as pd

FILE = './data_weather/visualcrossing.csv'
CONFIG_FILE = 'Config_file.toml'

def modify_loc(location: str) -> str:
    '''
    Shortens the name of location to only city name
    '''
    return location.split(',')[0]

def night_hours(data: pd.DataFrame, ax1: Any, ax2: Any) -> None:
    ''' Marks hours between 22 PM and 6 AM as 'night hours'. '''
    sunrise, sunset = get_daylight_hours(CONFIG_FILE)
    sunrise = sunrise.split(':')
    sunset = sunset.split(':')
    for i in range(len(data.index) - 1):
        current_time = data.index[i]
        next_time = data.index[i + 1]

        if (current_time.hour >= int(sunset[0]) or current_time.hour < int(sunrise[0])):
            ax1.axvspan(current_time, next_time, facecolor='#333333', alpha=0.2)
            ax2.axvspan(current_time, next_time, facecolor='#333333', alpha=0.2)

def get_data(hours: int) -> pd.DataFrame:
    '''
    Loads data from specified *.csv file for given number of hours. 
    Returns 'DataFrame' object.
    '''
    columns = ['name', 'datetime', 'temp', 'feelslike', 'winddir','windspeed', 
            'windgust', 'precip', 'snow', 'cloudcover' ]
    with open(FILE, encoding='utf-8') as reader:
        data = pd.read_csv(reader, 
                        usecols=columns,
                        index_col='datetime',
                        parse_dates=True                       
                        )

    data['name'] = data['name'].apply(modify_loc)

    data = data.iloc[12:hours+12]
    return data

def main():
    data = get_data(56)
  
    fig, ax = plt.subplots(2, 1, figsize=(15,6), layout='constrained')
    sns.set_style("whitegrid")

    # TOP Graph

    # Wind and wind gusts
    ax_left_up = ax[0]
    wind = ax_left_up.bar(data.index, data['windspeed'], width=0.04, color='green', label='Prędkość wiatru')
    gust = ax_left_up.scatter(data.index, data['windgust'], c='steelblue', marker='_', s=100, label='Porywy wiatru')

    ax_left_up.set_title(f'Prognoza na następne 48h dla {data["name"].iloc[0]}')
    ax_left_up.set_ylabel('Prędkość wiatru (km/h)')

    # Set temp readout on one graph
    ax_right_up = ax_left_up.twinx()
    ax_right_up.plot(data.index, data['temp'], color='darkred', label="Temperatura")
    ax_right_up.plot(data.index, data['feelslike'], color='pink', label='Temperatura odczuwalna')
    ax_right_up.set_ylabel('Temperatura (°C)', color='red')
    ax_right_up.tick_params(axis='y', labelcolor='red')

    # Setting X axis labels for the upper graph
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H'))  # Format as day-month hour

    # Zmieniamy lokalizator główny na godziny co 2 (parzyste godziny)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 2)))

    # Pozostawiamy lokalizator mniejszy co godzinę
    ax[0].xaxis.set_minor_locator(mdates.HourLocator())  
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Grid
    ax[0].grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    ax[0].grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    # Filling color between 'temp' and 'feelslike'
    ax_right_up.fill_between(data.index, data['temp'], data['feelslike'], 
                            where=(data['temp'] != data['feelslike']),
                            color='salmon', alpha=0.2)

    # Arrows pointing wind direction
    arrow_length = 1.5  
    arrow_y = data['windspeed'].mean() + 15

    for i in range(len(data)):
        wind_dir_rad = np.deg2rad(data['winddir'].iloc[i]) 
        x = data.index[i]
        dy = arrow_length * np.sin(wind_dir_rad)  
        ax_right_up.annotate('', xy=(x + pd.Timedelta(hours=0.1), arrow_y + dy), xytext=(x, arrow_y),
                            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    # Lower Graph
    ax_left_dwn = ax[1]
    ax_left_dwn.bar(data.index, data['cloudcover'], width=0.04, color='lightblue', label="Chmury")  
    ax_left_dwn.set_title('Zachmurzenie')
    ax_left_dwn.set_ylabel('Pokrywa chmur (%)')

    ax_right_dwn = ax_left_dwn.twinx()
    ax_right_dwn.bar(data.index, data['precip'], width=0.02, color='blue', label='Opady deszczu')
    ax_right_dwn.bar(data.index, data['snow'], width=0.02, color='red', label='Opady śniegu')

    ax_right_dwn.set_ylabel('Opady (mm)', color='gray')
    ax_right_dwn.set_ylim(bottom=0)
    ax_right_dwn.tick_params(axis='y', labelcolor='black')

    # Setting axis labels for the lower graph
    ax_left_dwn.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H'))  # Format as day-month hour

    # Zmieniamy lokalizator główny na godziny co 2 (parzyste godziny)
    ax_left_dwn.xaxis.set_major_locator(mdates.HourLocator(byhour=range(0, 24, 2)))

    # Pozostawiamy lokalizator mniejszy co godzinę
    ax_left_dwn.xaxis.set_minor_locator(mdates.HourLocator())  
    plt.setp(ax_left_dwn.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Grid
    ax_left_dwn.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
    ax_right_dwn.grid(which='minor', linestyle=':', linewidth='0.5', color='orange')

    # Created 'Wind Direction Marker' 
    arrow_legend = Line2D([0], [0], color='red', lw=0.5, marker='>', markersize=5, label='Kierunek wiatru')

    # Legends
    ax[0].legend(handles=(wind, gust, arrow_legend), loc='upper left')
    ax_right_up.legend(loc='upper right')
    ax_left_dwn.legend(loc='upper left')
    ax_right_dwn.legend(loc='upper right')

    night_hours(data, ax[0], ax[1])

    return plt

if __name__ == '__main__':
    plt = main()
    plt.savefig('weather_plot.png')
    plt.show()
else:
    plt = main()
    plt.savefig('weather_plot.png')
    plt.close()
