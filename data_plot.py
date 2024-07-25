import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

data = data.head(72)


sns.set_style("whitegrid")


fig, ax = plt.subplots(2, 1, figsize=(15,6), layout='constrained' )

ax[0].bar(data.index, data['windspeed'],width=0.05, color='darkblue', label='Prędkosć wiatru')
ax[0].scatter(data.index, data['windgust'], c='steelblue', marker='_',s=100, label='Porywy wiatru')

ax[0].set_title('Prędkość i porywy wiatru')
ax[0].set_xlabel('Dzień')
ax[0].set_ylabel('Prędkość wiatru (m/s)')

#setting axis labels
ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
ax[0].xaxis.set_major_locator(mdates.HourLocator(interval=6))  
ax[0].xaxis.set_minor_locator(mdates.HourLocator())  
plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45, ha='right')

#grid
ax[0].grid(which='major', linestyle='-', linewidth='0.5', color='gray')
ax[0].grid(which='minor', linestyle=':', linewidth='0.5', color='gray')


ax[0].legend()



ax[1].plot(data.index, data['temp'], color='red', label="Temperatura")
ax[1].scatter(data.index, data['feelslike'], color='orange', label='Temperatura odczuwalna')
ax[1].set_title('Temperatura')
ax[1].set_xlabel('Dzień')
ax[1].set_ylabel('Temperatura (°C)')

#setting axis labels
ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m %H:%M'))
ax[1].xaxis.set_major_locator(mdates.HourLocator(interval=6))  
ax[1].xaxis.set_minor_locator(mdates.HourLocator())  
plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=45, ha='right')

#grid
ax[1].grid(which='major', linestyle='-', linewidth='0.5', color='gray')
ax[1].grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

ax[1].legend()

# night hours
for i in range(len(data.index) - 1):
    current_time = data.index[i]
    next_time = data.index[i + 1]
    
   
    if (current_time.hour >= 22 or current_time.hour < 6):
        ax[0].axvspan(current_time, next_time, facecolor='blue', alpha=0.2)
        ax[1].axvspan(current_time, next_time, facecolor='blue', alpha=0.2)





plt.show()
