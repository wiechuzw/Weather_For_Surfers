import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FILE ='DATA/data.csv'

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

data = data.tail(72)


fig, ax = plt.subplots(figsize=(10, 5), layout='constrained')
data['windspeed'].plot(ax=ax, style='_', label='Windspeed', color='red', lw=40)
data['windgust'].plot(ax=ax, style='_', label='Windgust', color='darkblue')
ax.set_xlabel('Date')
ax.set_ylabel('Windspeed')

# ax.legend()

ax2 = ax.twinx()
ax2.set_ylabel('Temperature °C')
ax2.set_ylabel('Temperature')
data['temp'].plot(ax=ax2, style='-', label= 'Temperature', color='green')
# ax2.legend()
fig.legend(loc='upper left', bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)

plt.show()