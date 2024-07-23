import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

FILE ='./data_weather/visualcrossing.csv'

def modify_loc(location:str)->str:
    '''
    Shortens the name of location to only city name
    '''
    return location.split(',')[0]


columns = ['name', 'datetime', 'temp', 'feelslike', 'precip', 'winddir','windspeed', 'windgust', 'sealevelpressure' ]
with open(FILE, encoding='utf-8') as reader:
    data = pd.read_csv(reader, 
                       usecols=columns,
                       index_col='datetime',
                       parse_dates=True                       
                       )


data['name'] = data['name'].apply(modify_loc)

# data = data.tail(72)


sns.set_style("whitegrid")
## Ver 1.0

# fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
# data['windspeed'].plot(ax=ax, style='_', label='Windspeed', color='red', lw=40)
# data['windgust'].plot(ax=ax, style='_', label='Windgust', color='darkblue')
# ax.set_xlabel('Date')
# ax.set_ylabel('Windspeed')


# ax2 = ax.twinx()
# ax2.set_ylabel('Temperature °C')
# ax2.set_ylabel('Temperature')
# data['temp'].plot(ax=ax2, style='-', label= 'Temperature', color='green')
# # ax2.legend()
# fig.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)

## Ver 2.0

fig, ax = plt.subplots(2, 1, figsize=(15,6), layout='constrained' )

ax[0].bar(data.index, data['windspeed'],width=0.1, color='darkblue')
ax[0].scatter(data.index, data['windgust'], c='steelblue', marker='_',s=10, label='Porywy wiatru')

ax[0].set_title('Prędkość i porywy wiatru')
ax[0].set_xlabel('Data')
ax[0].set_ylabel('Prędkość wiatru (m/s)')



ax[1].plot(data.index, data['temp'], color='red')
ax[1].scatter(data.index, data['feelslike'], color='orange')
ax[1].set_title('Temperatura')
ax[1].set_xlabel('Data')
ax[1].set_ylabel('Temperatura (°C)')


plt.show()
