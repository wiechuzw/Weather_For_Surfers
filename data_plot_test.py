## AAA Wyświetlanie x dni do przodu
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sunrise_sunset import get_daylight_hours


# Przykładowa liczba dni, która określa do kiedy ma sięgać zakres (np. 2 dni - od dziś do pojutrza)
number_days_ahead = 2

# Plik konfiguracyjny zawierający współrzędne geograficzne
config_file = 'Config_file.toml'

# Pobieranie daty początkowej (dzisiejszy wschód słońca) i końcowej (zachód za 'days_to_add' dni)
start_sunrise, _ = get_daylight_hours(config_file, datetime.now().strftime('%Y-%m-%d'))
_, end_sunset = get_daylight_hours(config_file, (datetime.now() + timedelta(days=number_days_ahead)).strftime('%Y-%m-%d'))

# Konwersja godzin wschodu i zachodu na pełne daty
start_datetime = datetime.now().replace(hour=int(start_sunrise.split(':')[0]), minute=int(start_sunrise.split(':')[1]), second=0)
end_datetime = (datetime.now() + timedelta(days=number_days_ahead)).replace(hour=int(end_sunset.split(':')[0]), minute=int(end_sunset.split(':')[1]), second=0)

# Wczytanie danych z pliku CSV
df = pd.read_csv('data_weather/visualcrossing.csv')

# Filtrowanie danych na podstawie zakresu dat
filtered_df = df[(pd.to_datetime(df['datetime']) >= start_datetime) & (pd.to_datetime(df['datetime']) <= end_datetime)]

# Współrzędne X (czas) i Y (poziom wiatru)
time_range = pd.to_datetime(filtered_df['datetime'])
x = np.arange(len(time_range))
y = np.zeros_like(x)  # Wszystkie strzałki w tej samej linii

# Kąty wiatru
angle = filtered_df['winddir'].values

# Przekształcenie kąta w taki sposób, aby pasował do kierunków wiatru
adjusted_angle = (270 - angle) % 360  # Obracamy o 270 stopni w prawo
adjusted_angle_rad = np.deg2rad(adjusted_angle)  # Przekształcenie na radiany

# Stała długość strzałek
length = 0.6

# Komponenty wektora w osi X i Y (długość jest stała)
u = length * np.cos(adjusted_angle_rad)
v = length * np.sin(adjusted_angle_rad)

# Tworzenie wykresu
plt.figure(figsize=(18, 5))
ax = plt.gca()

# Ustawienie proporcji osi na 'equal', aby X i Y miały tę samą skalę
ax.set_aspect('equal')

# Rysowanie strzałek
plt.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue')

# Ustawienia osi X
plt.xticks(ticks=x, labels=[t.strftime('%d %H') for t in time_range], rotation=60)
plt.xlabel('Dzień m-ca / godzina')
plt.ylabel('Pozycja')
plt.title(f'Kierunki wiatru od wschodu słońca dzisiaj do zachodu za {number_days_ahead} dni')

plt.xlim(-1, len(time_range))
plt.ylim(-1, 1)

plt.show()
  


### BBB Suwak / wykres 1 + 2 dni / zakres 15 dni do przodu
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sunrise_sunset import get_daylight_hours
from matplotlib.widgets import Slider

# Przykładowa liczba dni, która określa do kiedy ma sięgać zakres (np. 15 dni - od dziś do za 15 dni)
number_days_ahead = 15

# Okres wyświetlany jednocześnie (np. 3 dni)
display_days = 2

# Plik konfiguracyjny zawierający współrzędne geograficzne
config_file = 'Config_file.toml'

# Pobieranie daty początkowej (dzisiejszy wschód słońca) i końcowej (zachód za 'number_days_ahead' dni)
start_sunrise, _ = get_daylight_hours(config_file, datetime.now().strftime('%Y-%m-%d'))
_, end_sunset = get_daylight_hours(config_file, (datetime.now() + timedelta(days=number_days_ahead)).strftime('%Y-%m-%d'))

# Konwersja godzin wschodu i zachodu na pełne daty
start_datetime = datetime.now().replace(hour=int(start_sunrise.split(':')[0]), minute=int(start_sunrise.split(':')[1]), second=0)
end_datetime = (datetime.now() + timedelta(days=number_days_ahead)).replace(hour=int(end_sunset.split(':')[0]), minute=int(end_sunset.split(':')[1]), second=0)

# Wczytanie danych z pliku CSV
df = pd.read_csv('data_weather/visualcrossing.csv')

# Filtrowanie danych na podstawie zakresu dat
filtered_df = df[(pd.to_datetime(df['datetime']) >= start_datetime) & (pd.to_datetime(df['datetime']) <= end_datetime)]

# Współrzędne X (czas) i Y (poziom wiatru)
time_range = pd.to_datetime(filtered_df['datetime'])
x = np.arange(len(time_range))
y = np.zeros_like(x)  # Wszystkie strzałki w tej samej linii

# Kąty wiatru
angle = filtered_df['winddir'].values

# Przekształcenie kąta w taki sposób, aby pasował do kierunków wiatru
adjusted_angle = (270 - angle) % 360  # Obracamy o 270 stopni w prawo
adjusted_angle_rad = np.deg2rad(adjusted_angle)  # Przekształcenie na radiany

# Stała długość strzałek
length = 0.6

# Komponenty wektora w osi X i Y (długość jest stała)
u = length * np.cos(adjusted_angle_rad)
v = length * np.sin(adjusted_angle_rad)

# Tworzenie wykresu
fig, ax = plt.subplots(figsize=(18, 5))
plt.subplots_adjust(bottom=0.2)  # Miejsce na slider

# Rysowanie strzałek
quiver = ax.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue')

# Ustawienia osi X i osi Y
ax.set_aspect('equal')
plt.xlabel('Dzień miesiąca Godzina')
plt.ylabel('Pozycja')
plt.title(f'Kierunek wiatru od wschodu słońca dzisiaj do zachodu za {number_days_ahead} dni')
plt.ylim(-1, 1)

# Zakres początkowy na wykresie (wyświetla np. pierwsze 3 dni)
start_index = 0
end_index = min(len(time_range), display_days * 24)  # Display 3 dni (24 godziny na dzień)

ax.set_xlim(start_index, end_index)

# Ustawianie ticków co 2 godziny i etykiet
visible_ticks = np.arange(start_index, end_index, 2)  # Co 2 godziny
visible_labels = [t.strftime('%d %H') for t in time_range[start_index:end_index:2]]  # Co 2 godziny
ax.set_xticks(visible_ticks)
ax.set_xticklabels(visible_labels, rotation=45)

# Funkcja aktualizująca wykres przy zmianie suwaka
def update(val):
    start_index = int(slider.val)
    end_index = min(start_index + display_days * 24, len(time_range))
    ax.set_xlim(start_index, end_index)
    visible_ticks = np.arange(start_index, end_index, 2)  # Co 2 godziny
    visible_labels = [t.strftime('%d %H:%M') for t in time_range[start_index:end_index:2]]
    ax.set_xticks(visible_ticks)
    ax.set_xticklabels(visible_labels, rotation=45)
    fig.canvas.draw_idle()

# Tworzenie slidera
ax_slider = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Przesuń', 0, len(time_range) - display_days * 24, valinit=0, valstep=1)

# Aktualizacja przy zmianie wartości slidera
slider.on_changed(update)

plt.show()

### Suwak / wykres 1 + 2 dni / zakres 15 dni do przodu
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from datetime import datetime, timedelta
# from sunrise_sunset import get_daylight_hours
# from matplotlib.widgets import Slider

# # Przykładowa liczba dni, która określa do kiedy ma sięgać zakres (np. 15 dni - od dziś do za 15 dni)
# number_days_ahead = 15

# # Okres wyświetlany jednocześnie (np. 3 dni)
# display_days = 2

# # Plik konfiguracyjny zawierający współrzędne geograficzne
# config_file = 'Config_file.toml'

# # Pobieranie daty początkowej (dzisiejszy wschód słońca) i końcowej (zachód za 'number_days_ahead' dni)
# start_sunrise, _ = get_daylight_hours(config_file, datetime.now().strftime('%Y-%m-%d'))
# _, end_sunset = get_daylight_hours(config_file, (datetime.now() + timedelta(days=number_days_ahead)).strftime('%Y-%m-%d'))

# # Konwersja godzin wschodu i zachodu na pełne daty
# start_datetime = datetime.now().replace(hour=int(start_sunrise.split(':')[0]), minute=int(start_sunrise.split(':')[1]), second=0)
# end_datetime = (datetime.now() + timedelta(days=number_days_ahead)).replace(hour=int(end_sunset.split(':')[0]), minute=int(end_sunset.split(':')[1]), second=0)

# # Wczytanie danych z pliku CSV
# df = pd.read_csv('data_weather/visualcrossing.csv')

# # Filtrowanie danych na podstawie zakresu dat
# filtered_df = df[(pd.to_datetime(df['datetime']) >= start_datetime) & (pd.to_datetime(df['datetime']) <= end_datetime)]

# # Współrzędne X (czas) i Y (poziom wiatru)
# time_range = pd.to_datetime(filtered_df['datetime'])
# x = np.arange(len(time_range))
# y = np.zeros_like(x)  # Wszystkie strzałki w tej samej linii

# # Kąty wiatru
# angle = filtered_df['winddir'].values

# # Przekształcenie kąta w taki sposób, aby pasował do kierunków wiatru
# adjusted_angle = (270 - angle) % 360  # Obracamy o 270 stopni w prawo
# adjusted_angle_rad = np.deg2rad(adjusted_angle)  # Przekształcenie na radiany

# # Stała długość strzałek
# length = 0.5

# # Komponenty wektora w osi X i Y (długość jest stała)
# u = length * np.cos(adjusted_angle_rad)
# v = length * np.sin(adjusted_angle_rad)

# # Tworzenie wykresu
# fig, ax = plt.subplots(figsize=(12, 5))
# plt.subplots_adjust(bottom=0.25)  # Miejsce na slidera

# # Rysowanie strzałek
# quiver = ax.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue')

# # Ustawienia osi X i osi Y
# ax.set_aspect('equal')
# plt.xlabel('Dzień miesiąca Godzina')
# plt.ylabel('Pozycja')
# plt.title(f'Kierunek wiatru od wschodu słońca dzisiaj do zachodu za {number_days_ahead} dni')
# plt.ylim(-1, 1)

# # Zakres początkowy na wykresie (wyświetla np. pierwsze 3 dni)
# start_index = 0
# end_index = min(len(time_range), display_days * 24)  # Display 3 dni (24 godziny na dzień)

# ax.set_xlim(start_index, end_index)

# # Ustawianie ticków co 2 godziny i etykiet
# visible_ticks = np.arange(start_index, end_index, 2)  # Co 2 godziny
# visible_labels = [t.strftime('%d %H') for t in time_range[start_index:end_index:2]]  # Co 2 godziny
# ax.set_xticks(visible_ticks)
# ax.set_xticklabels(visible_labels, rotation=45)

# # Dodawanie slidera do przewijania wykresu
# ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])  # Pozycja i rozmiar slidera
# slider = Slider(ax_slider, 'Shift', 0, len(time_range) - display_days * 24, valinit=0, valstep=1)

# def update(val):
#     shift = int(slider.val)
#     ax.set_xlim(shift, shift + display_days * 24)  # Przesuwanie osi X
#     ax.set_xticks(np.arange(shift, shift + display_days * 24, 2))  # Ustawianie ticków co 2 godziny
#     ax.set_xticklabels([t.strftime('%d %H:%M') for t in time_range[shift:shift + display_days * 24:2]], rotation=45)
#     fig.canvas.draw_idle()  # Odświeżenie wykresu

# slider.on_changed(update)

# # Wyświetlanie wykresu
# plt.show()


### Suwak / wykres 1 + 2 dni / zakres 15 dni do przodu
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from datetime import datetime, timedelta
# from sunrise_sunset import get_daylight_hours
# from matplotlib.widgets import Slider

# # Przykładowa liczba dni, która określa do kiedy ma sięgać zakres (np. 15 dni - od dziś do za 15 dni)
# number_days_ahead = 15

# # Okres wyświetlany jednocześnie (np. 3 dni)
# display_days = 2

# # Plik konfiguracyjny zawierający współrzędne geograficzne
# config_file = 'Config_file.toml'

# # Pobieranie daty początkowej (dzisiejszy wschód słońca) i końcowej (zachód za 'number_days_ahead' dni)
# start_sunrise, _ = get_daylight_hours(config_file, datetime.now().strftime('%Y-%m-%d'))
# _, end_sunset = get_daylight_hours(config_file, (datetime.now() + timedelta(days=number_days_ahead)).strftime('%Y-%m-%d'))

# # Konwersja godzin wschodu i zachodu na pełne daty
# start_datetime = datetime.now().replace(hour=int(start_sunrise.split(':')[0]), minute=int(start_sunrise.split(':')[1]), second=0)
# end_datetime = (datetime.now() + timedelta(days=number_days_ahead)).replace(hour=int(end_sunset.split(':')[0]), minute=int(end_sunset.split(':')[1]), second=0)

# # Wczytanie danych z pliku CSV
# df = pd.read_csv('data_weather/visualcrossing.csv')

# # Filtrowanie danych na podstawie zakresu dat
# filtered_df = df[(pd.to_datetime(df['datetime']) >= start_datetime) & (pd.to_datetime(df['datetime']) <= end_datetime)]

# # Współrzędne X (czas) i Y (poziom wiatru)
# time_range = pd.to_datetime(filtered_df['datetime'])
# x = np.arange(len(time_range))
# y = np.zeros_like(x)  # Wszystkie strzałki w tej samej linii

# # Kąty wiatru
# angle = filtered_df['winddir'].values

# # Przekształcenie kąta w taki sposób, aby pasował do kierunków wiatru
# adjusted_angle = (270 - angle) % 360  # Obracamy o 270 stopni w prawo
# adjusted_angle_rad = np.deg2rad(adjusted_angle)  # Przekształcenie na radiany

# # Stała długość strzałek
# length = 0.5

# # Komponenty wektora w osi X i Y (długość jest stała)
# u = length * np.cos(adjusted_angle_rad)
# v = length * np.sin(adjusted_angle_rad)

# # Tworzenie wykresu
# fig, ax = plt.subplots(figsize=(12, 5))
# plt.subplots_adjust(bottom=0.25)  # Miejsce na slidera

# # Rysowanie strzałek
# quiver = ax.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue')

# # Ustawienia osi X i osi Y
# ax.set_aspect('equal')
# plt.xlabel('Dzień miesiąca Godzina')
# plt.ylabel('Pozycja')
# plt.title(f'Kierunek wiatru - {number_days_ahead} dni')
# plt.ylim(-1, 1)

# # Zakres początkowy na wykresie (wyświetla np. pierwsze 3 dni)
# start_index = 0
# end_index = min(len(time_range), display_days * 24)  # Display 3 dni (24 godziny na dzień)

# ax.set_xlim(start_index, end_index)

# # Ustawianie ticków co 2 godziny i etykiet
# visible_ticks = np.arange(start_index, end_index, 2)  # Co 2 godziny
# visible_labels = [t.strftime('%d %H') for t in time_range[start_index:end_index:2]]  # Co 2 godziny
# ax.set_xticks(visible_ticks)
# ax.set_xticklabels(visible_labels, rotation=45)

# # Dodawanie slidera do przewijania wykresu
# ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])  # Pozycja i rozmiar slidera
# slider = Slider(ax_slider, 'Shift', 0, len(time_range) - display_days * 24, valinit=0, valstep=1)

# # Funkcja aktualizująca wykres
# def update(val):
#     shift = int(slider.val)
#     ax.set_xlim(shift, shift + display_days * 24)  # Przesuwanie osi X
#     ax.set_xticks(np.arange(shift, shift + display_days * 24, 2))  # Ustawianie ticków co 2 godziny
#     ax.set_xticklabels([t.strftime('%d %H') for t in time_range[shift:shift + display_days * 24:2]], rotation=45)
    
#     # Ustawienie ticków i etykiet dla suwaka
#     slider_ticks = np.arange(0, number_days_ahead + 1)  # Ustaw ticki co 1 dzień
#     slider_labels = [(datetime.now() + timedelta(days=i)).strftime('%d') for i in range(number_days_ahead + 1)]
    
#     # Ustawienie etykiet
#     ax_slider.set_xticks(slider_ticks)
#     ax_slider.set_xticklabels(slider_labels)  # Ustawienie etykiet z dniami

#     fig.canvas.draw_idle()  # Odświeżenie wykresu

# slider.on_changed(update)

# # Wyświetlanie wykresu
# plt.show()




### Suwak / wykres 1 + 2 dni / zakres 15 dni do przodu
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# from datetime import datetime, timedelta
# from sunrise_sunset import get_daylight_hours
# from matplotlib.widgets import Slider

# # Przykładowa liczba dni, która określa do kiedy ma sięgać zakres (np. 15 dni - od dziś do za 15 dni)
# number_days_ahead = 15

# # Okres wyświetlany jednocześnie (np. 3 dni)
# display_days = 2

# # Plik konfiguracyjny zawierający współrzędne geograficzne
# config_file = 'Config_file.toml'

# # Pobieranie daty początkowej (dzisiejszy wschód słońca) i końcowej (zachód za 'number_days_ahead' dni)
# start_sunrise, _ = get_daylight_hours(config_file, datetime.now().strftime('%Y-%m-%d'))
# _, end_sunset = get_daylight_hours(config_file, (datetime.now() + timedelta(days=number_days_ahead)).strftime('%Y-%m-%d'))

# # Konwersja godzin wschodu i zachodu na pełne daty
# start_datetime = datetime.now().replace(hour=int(start_sunrise.split(':')[0]), minute=int(start_sunrise.split(':')[1]), second=0)
# end_datetime = (datetime.now() + timedelta(days=number_days_ahead)).replace(hour=int(end_sunset.split(':')[0]), minute=int(end_sunset.split(':')[1]), second=0)

# # Wczytanie danych z pliku CSV
# df = pd.read_csv('data_weather/visualcrossing.csv')

# # Filtrowanie danych na podstawie zakresu dat
# filtered_df = df[(pd.to_datetime(df['datetime']) >= start_datetime) & (pd.to_datetime(df['datetime']) <= end_datetime)]

# # Współrzędne X (czas) i Y (poziom wiatru)
# time_range = pd.to_datetime(filtered_df['datetime'])
# x = np.arange(len(time_range))
# y = np.zeros_like(x)  # Wszystkie strzałki w tej samej linii

# # Kąty wiatru
# angle = filtered_df['winddir'].values

# # Przekształcenie kąta w taki sposób, aby pasował do kierunków wiatru
# adjusted_angle = (270 - angle) % 360  # Obracamy o 270 stopni w prawo
# adjusted_angle_rad = np.deg2rad(adjusted_angle)  # Przekształcenie na radiany

# # Stała długość strzałek
# length = 0.5

# # Komponenty wektora w osi X i Y (długość jest stała)
# u = length * np.cos(adjusted_angle_rad)
# v = length * np.sin(adjusted_angle_rad)

# # Tworzenie wykresu
# fig, ax = plt.subplots(figsize=(12, 5))
# plt.subplots_adjust(bottom=0.25)  # Miejsce na slidera

# # Rysowanie strzałek
# quiver = ax.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue')

# # Ustawienia osi X i osi Y
# ax.set_aspect('equal')
# plt.xlabel('Dzień miesiąca Godzina')
# plt.ylabel('Pozycja')
# plt.title(f'Kierunek wiatru od wschodu słońca dzisiaj do zachodu za {number_days_ahead} dni')
# plt.ylim(-1, 1)

# # Zakres początkowy na wykresie (wyświetla np. pierwsze 3 dni)
# start_index = 0
# end_index = min(len(time_range), display_days * 24)  # Display 3 dni (24 godziny na dzień)

# ax.set_xlim(start_index, end_index)

# # Ustawianie ticków co 2 godziny i etykiet
# visible_ticks = np.arange(start_index, end_index, 2)  # Co 2 godziny
# visible_labels = [t.strftime('%d %H') for t in time_range[start_index:end_index:2]]  # Co 2 godziny
# ax.set_xticks(visible_ticks)
# ax.set_xticklabels(visible_labels, rotation=45)

# # Dodawanie slidera do przewijania wykresu
# ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03])  # Pozycja i rozmiar slidera
# slider = Slider(ax_slider, 'Shift', 0, len(time_range) - display_days * 24, valinit=0, valstep=1)

# # Funkcja aktualizująca wykres
# def update(val):
#     shift = int(slider.val)
#     ax.set_xlim(shift, shift + display_days * 24)  # Przesuwanie osi X
#     ax.set_xticks(np.arange(shift, shift + display_days * 24, 2))  # Ustawianie ticków co 2 godziny
#     ax.set_xticklabels([t.strftime('%d %H') for t in time_range[shift:shift + display_days * 24:2]], rotation=45)
    
#     fig.canvas.draw_idle()  # Odświeżenie wykresu

# slider.on_changed(update)

# # Wyświetlanie wykresu
# plt.show()
