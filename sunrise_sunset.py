import requests
import toml
from datetime import datetime, timedelta
import pytz  # Import pytz for timezone handling

def read_coordinates(file: str):
    """
    Reads the latitude and longitude from a configuration file in TOML format.
    """
    config = toml.load(file)
    return config['latitude'], config['longitude']

def get_daylight_hours(file: str, date: str = None):
    """
    Finds the sunrise and sunset times for a given date and rounds them to full hours with half-hour accuracy.
    If the date is not given, the data for the current day is provided.
    It finds sunrise and sunset time for a specific location according to the configuration file.
    The latitude and longitude (specific location) are loaded from a configuration file in TOML format.
    """
    lat, lon = read_coordinates(file)
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}&formatted=0"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure a successful response
        data = response.json()
        
        # Extract sunrise and sunset times in UTC
        sunrise_utc = data['results']['sunrise']
        sunset_utc = data['results']['sunset']
        
        # Convert from UTC to local time (Europe/Warsaw)
        local_tz = pytz.timezone('Europe/Warsaw')
        sunrise = datetime.fromisoformat(sunrise_utc).astimezone(local_tz)
        sunset = datetime.fromisoformat(sunset_utc).astimezone(local_tz)
        
        # Rounding to whole hours
        sunrise = (sunrise + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)
        sunset = (sunset + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)

        return sunrise.strftime('%H:%M'), sunset.strftime('%H:%M')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sunrise and sunset data: {e}")
        return None, None

def main():
    config_file = 'Config_file.toml'
    sunrise, sunset = get_daylight_hours(config_file)
    if sunrise and sunset:
        print(f"Sunrise: {sunrise}, Sunset: {sunset}")
    else:
        print("Failed to fetch sunrise and sunset times.")

if __name__ == '__main__':
    main()