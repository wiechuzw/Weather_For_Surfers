import pandas as pd
from datetime import datetime, timedelta
import sunrise_sunset

def read_border_values(file: str):
    """
    Loading border values from a configuration file.
    """
    with open(file, 'r', encoding='utf-8') as reader:
        values = {}
        for line in reader:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=')
                values[key.strip()] = float(value.strip())
    return values

def load_weather_data(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df

def check_weather_conditions(df, sunrise, sunset, min_windspeed, max_windspeed, min_temp):
    """
    Checking if the weather conditions are suitable between sunrise and sunset
    """
    # Converting sunrise and sunset times to datetime ignoring minutes
    sunrise_time = datetime.strptime(sunrise, '%H:%M').replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    sunset_time = datetime.strptime(sunset, '%H:%M').replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    
    # Adjustment to whole hours (no minutes)
    sunrise_time = sunrise_time.replace(minute=0)
    sunset_time = sunset_time.replace(minute=0)
    
    # Filtering data to the period between sunrise and sunset
    df_day = df[(df['datetime'] >= sunrise_time) & (df['datetime'] <= sunset_time)]
    
    # Checking weather conditions (wind speed and temperature)
    condition = df_day[(df_day['windspeed'] >= min_windspeed) & 
                       (df_day['windspeed'] <= max_windspeed) & 
                       (df_day['temp'] > min_temp)]
    
    return not condition.empty


def main():
    weather_file_path = 'data_weather/visualcrossing.csv'
    config_file = 'border_values.txt'
    
    df = load_weather_data(weather_file_path)
    
    # Loading border values
    border_values = read_border_values(config_file)
    min_windspeed = border_values.get('min_windspeed', 11)  
    max_windspeed = border_values.get('max_windspeed', 60)
    min_temp = border_values.get('temp_min', 5)  
    
    # Get sunrise and sunset times for two days
    sunrise_tomorrow, sunset_tomorrow = sunrise_sunset.get_daylight_hours(config_file, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
    sunrise_day_after, sunset_day_after = sunrise_sunset.get_daylight_hours(config_file, (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'))
    
    # Checking the weather conditions separately for tomorrow and the day after tomorrow
    surfing_conditions_tomorrow = check_weather_conditions(df, sunrise_tomorrow, sunset_tomorrow, min_windspeed, max_windspeed, min_temp)
    surfing_conditions_day_after = check_weather_conditions(df, sunrise_day_after, sunset_day_after, min_windspeed, max_windspeed, min_temp)
    
    # Deciding which message to print based on the weather conditions
    if surfing_conditions_tomorrow:
        print("It looks like the wind is coming -> tomorow")
    elif surfing_conditions_day_after:
        print("After tomorrow cool wind will be expected")
    else:
        print("Weather conditions worse than required")

if __name__ == '__main__':
    main()