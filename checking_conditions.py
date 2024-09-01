import pandas as pd
from datetime import datetime, timedelta
import sunrise_sunset  # Upewnij się, że to jest zaktualizowana wersja
import toml
import sys

def read_border_values(file: str):
    """
    Loads border values from a TOML configuration file.
    """
    config = toml.load(file)
    print("Loaded configuration values:")
    print(config)  # Wyświetl załadowane wartości
    return {
        'min_windspeed': config.get('min_windspeed', 11),
        'max_windspeed': config.get('max_windspeed', 60),
        'temp_min': config.get('temp_min', 5)
    }

def load_weather_data(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    print("Loaded weather data:")
    print(df.head())  # Dodano: Wyświetl dane pogodowe
    return df

def parse_time(date_str, time_str):
    """
    Combines a date string and a time string into a datetime object.
    """
    full_datetime_str = f"{date_str}T{time_str}:00"
    return datetime.fromisoformat(full_datetime_str)

def check_weather_conditions(df, date, sunrise, sunset, min_windspeed, max_windspeed, min_temp):
    """
    Checking if the weather conditions are suitable between sunrise and sunset
    """
    sunrise_time = parse_time(date, sunrise)
    sunset_time = parse_time(date, sunset)

    print(f"Sunrise time: {sunrise_time}, Sunset time: {sunset_time}")

    df_day = df[(df['datetime'] >= sunrise_time) & (df['datetime'] <= sunset_time)]
    print(f"Filtered data between sunrise and sunset for {date}:")
    print(df_day[['datetime', 'windspeed']])

    condition = df_day[
        (df_day['windspeed'] >= min_windspeed) &
        (df_day['windspeed'] <= max_windspeed) &
        (df_day['temp'] >= min_temp)
    ]

    print("Weather conditions after checking:")
    print(condition[['datetime', 'windspeed', 'temp']])

    if not condition.empty:
        print(f"Suitable weather conditions found between {sunrise} and {sunset}.")
    else:
        print(f"No suitable weather conditions found between {sunrise} and {sunset}.")

    return not condition.empty

def main():
    weather_file_path = 'data_weather/visualcrossing.csv'
    config_file = 'Config_file.toml'
    
    df = load_weather_data(weather_file_path)
    
    # Loading border values
    border_values = read_border_values(config_file)
    min_windspeed = border_values.get('min_windspeed', 11)
    max_windspeed = border_values.get('max_windspeed', 60)
    min_temp = border_values.get('temp_min', 5)
    
    # Dates to check
    date_tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_day_after = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    
    # Get sunrise and sunset times for two days
    sunrise_tomorrow, sunset_tomorrow = sunrise_sunset.get_daylight_hours(config_file, date_tomorrow)
    sunrise_day_after, sunset_day_after = sunrise_sunset.get_daylight_hours(config_file, date_day_after)
    
    # Checking the weather conditions separately for tomorrow and the day after tomorrow
    print("\nChecking weather conditions for tomorrow...")
    surfing_conditions_tomorrow = check_weather_conditions(df, date_tomorrow, sunrise_tomorrow, sunset_tomorrow, min_windspeed, max_windspeed, min_temp)
    
    print("\nChecking weather conditions for the day after tomorrow...")
    surfing_conditions_day_after = check_weather_conditions(df, date_day_after, sunrise_day_after, sunset_day_after, min_windspeed, max_windspeed, min_temp)
    
    if surfing_conditions_tomorrow:
        print("It looks like the wind is coming -> tomorrow")
        sys.exit(0)  # Exit with code 0 if tomorrow's conditions are good
    elif surfing_conditions_day_after:
        print("After tomorrow cool wind will be expected")
        sys.exit(0)  # Exit with code 0 if the day after tomorrow's conditions are good
    else:
        print("Weather conditions worse than required")
        sys.exit(1)  # Exit with code 1 if no conditions are met

if __name__ == '__main__':
    main()