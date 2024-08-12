import requests
from datetime import datetime, timedelta


def read_coordinates(file: str):
    """
    Reads the latitude and longitude from a configuration file.
    """
    with open(file, 'r', encoding='utf-8') as reader:
        coordinates = {}
        for line in reader:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=')
                coordinates[key.strip()] = float(value.strip())
    return coordinates['latitude'], coordinates['longitude']


def get_daylight_hours(file: str, date: str = None):
    """
    This function finds the sunrise and sunset times for any date and rounds them to full hours with half-hour accuracy.
    If the date is not given, the data for the current day is given.
    This function finds sunrise and sunset time for a specific location according to the configuration file
    The latitude and longitude (specific location) are loading from a configuration file: border_valuse.py.
    """
    lat, lon = read_coordinates(file)
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')

    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}&formatted=0"
    
    response = requests.get(url)
    data = response.json()
    
    sunrise_utc = data['results']['sunrise']
    sunset_utc = data['results']['sunset']
    
    # Convert from UTC to local time
    sunrise = datetime.fromisoformat(sunrise_utc).astimezone()
    sunset = datetime.fromisoformat(sunset_utc).astimezone()
    
    # Rounding to whole hours
    sunrise = (sunrise + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)
    sunset = (sunset + timedelta(minutes=30)).replace(minute=0, second=0, microsecond=0)

    return sunrise.strftime('%H:%M'), sunset.strftime('%H:%M')


def main():
    config_file = 'border_values.txt'
    sunrise, sunset = get_daylight_hours(config_file)
    print(f"sunrise: {sunrise}, sunset: {sunset}")


if __name__ == '__main__':
    main()