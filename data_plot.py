from typing import Any

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import pandas as pd


FILE ='./data_weather/visualcrossing.csv'

def modify_loc(location:str)->str:
    '''
    Shortens the name of location to only city name
    '''
    return location.split(',')[0]

def night_hours(data: pd.DataFrame, ax1: Any, ax2: Any) -> None:
    for i in range(len(data.index) - 1):
        current_time = data.index[i]
        next_time = data.index[i + 1]
    
   
        if (current_time.hour >= 22 or current_time.hour < 6):
            ax1.axvspan(current_time, next_time, facecolor='blue', alpha=0.2)
            ax2.axvspan(current_time, next_time, facecolor='blue', alpha=0.2)


def get_data(hours: int)->pd.DataFrame:
    try :
        hours = int(hours)
    except ValueError:
        print('Function argument has to be given as integer!!!')


    columns = ['name', 'datetime', 'temp', 'feelslike', 'winddir','windspeed', 
            'windgust', 'precip', 'snow', 'cloudcover' ]
    with open(FILE, encoding='utf-8') as reader:
        data = pd.read_csv(reader, 
                        usecols=columns,
                        index_col='datetime',
                        parse_dates=True                       
                        )


    data['name'] = data['name'].apply(modify_loc)

    data = data.iloc[:hours]
    return data


def main():
    data = get_data(54)

    sns.set_style("whitegrid")


    fig, ax = plt.subplots(2, 1, figsize=(15,6), layout='constrained' )

    # TOP Graph

    #wind and wind gusts
    ax_left_up = ax[0]
    wind = ax_left_up.bar(data.index, data['windspeed'],width=0.04, color='lightblue', label='Prędkosć wiatru')
    gust = ax_left_up.scatter(data.index, data['windgust'], c='steelblue', marker='_',s=100, label='Porywy wiatru')

    ax_left_up.set_title(f'Prognoza na następne 48h dla {data['name'].iloc[0]}')
    ax_left_up.set_xlabel('Dzień')
    ax_left_up.set_ylabel('Prędkość wiatru (km/h)')

    #set temp readout on one graph
    ax_right_up = ax_left_up.twinx()
    ax_right_up.plot(data.index, data['temp'], color='darkred', label="Temperatura")
    ax_right_up.plot(data.index, data['feelslike'], color='pink', label='Temperatura odczuwalna')
    ax_right_up.set_ylabel('Temperatura (°C)', color='red')
    ax_right_up.tick_params(axis='y', labelcolor='red')

    #setting X axis labels
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
    ax[0].xaxis.set_major_locator(mdates.HourLocator(interval=3))  
    ax[0].xaxis.set_minor_locator(mdates.HourLocator())  
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

    #grid
    ax[0].grid(which='major', linestyle='-', linewidth='0.5', color='gray')
    ax[0].grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    # Filling color between 'temp' and 'feelslike'
    ax_right_up.fill_between(data.index, data['temp'], data['feelslike'], 
                        where=(data['temp'] != data['feelslike']),
                        color='lightsalmon', alpha=0.5)
                    


    # Arrows pointing wind direction
    arrow_label = 'Kierunek wiatru'
    arrow_length = 1.5  
    arrow_y = data['windspeed'].median() + 10
    for i in range(len(data)):
        wind_dir_rad = np.deg2rad(data['winddir'].iloc[i]) 
        x = data.index[i]
        dx = arrow_length * np.cos(wind_dir_rad)  
        dy = - arrow_length * np.sin(wind_dir_rad)  
        ax_right_up.annotate('', xy=(x + pd.Timedelta(hours=0.1), arrow_y + dy), xytext=(x, arrow_y),
                        arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
        


    # Bottom Graph

    ax_left_dwn = ax[1]
    ax_left_dwn.bar(data.index, data['cloudcover'], width=0.04,color='darkblue', label="Chmury")
    ax_left_dwn.set_title('Zachmurzenie')
    ax_left_dwn.set_xlabel('Dzień')
    ax_left_dwn.set_ylabel('pokrywa chmur (%)')

    ax_right_dwn = ax_left_dwn.twinx()
    ax_right_dwn.bar(data.index, data['precip'], color='orange', label='Opady deszczu')
    ax_right_dwn.bar(data.index, data['snow'], color= 'lightblue', label = 'Opady śniegu' )

    ax_right_dwn.set_ylabel('Opady (mm)', color='gray')
    ax_right_dwn.set_ylim(bottom=0)
    ax_right_dwn.tick_params(axis='y', labelcolor='black')


    #setting axis labels
    ax_left_dwn.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
    ax_left_dwn.xaxis.set_major_locator(mdates.HourLocator(interval=3))  
    ax_left_dwn.xaxis.set_minor_locator(mdates.HourLocator())  
    plt.setp(ax_left_dwn.xaxis.get_majorticklabels(), rotation=45, ha='right')

    #grid
    ax_left_dwn.grid(which='major', linestyle='-', linewidth='0.5', color='blue')
    ax_right_dwn.grid(which='minor', linestyle=':', linewidth='0.5', color='orange')


    # Created 'Wind Direction Marker' 
    arrow_legend = Line2D([0], [0], color='red', lw=0.5, marker='>', markersize=5, label='Kierunek wiatru')

    #Legends
    ax[0].legend(handles= (wind, gust,arrow_legend), loc='upper left')
    ax_right_up.legend(loc='upper right')
    ax_left_dwn.legend(loc='upper left')
    ax_right_dwn.legend(loc='upper right')


    night_hours(data, ax[0], ax[1])

    # plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
