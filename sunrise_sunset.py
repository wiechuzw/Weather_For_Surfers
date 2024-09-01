import requests
import toml
from datetime import datetime, timedelta
import pytz

def read_coordinates(file: str):
    """
    Reads the latitude and longitude from a configuration file in TOML format.
    """
    config = toml.load(file)
    return config['latitude'], config['longitude']

def get_daylight_hours(file: str, date: str = None):
    """
    Finds the sunrise and sunset times for a specific date and returns them rounded to full hours.
    If the date is not given, the current date is used.
    """
    lat, lon = read_coordinates(file)
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}&formatted=0"
    response = requests.get(url)
    data = response.json()
    
    # Convert from UTC to local time
    local_tz = pytz.timezone('Europe/Warsaw')  # Use your local timezone
    sunrise_utc = datetime.fromisoformat(data['results']['sunrise']).astimezone(local_tz)
    sunset_utc = datetime.fromisoformat(data['results']['sunset']).astimezone(local_tz)
    
    # Rounding to whole hours
    sunrise = (sunrise_utc + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)
    sunset = (sunset_utc + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)

    return sunrise.strftime('%H:%M'), sunset.strftime('%H:%M')

def main():
    config_file = 'Config_file.toml'
    sunrise, sunset = get_daylight_hours(config_file)
    print(f"Sunrise: {sunrise}, Sunset: {sunset}")

if __name__ == '__main__':
    main()
