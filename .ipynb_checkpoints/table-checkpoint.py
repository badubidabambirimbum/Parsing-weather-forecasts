import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import os


class table:

    def __init__(self):
        self.cities_url = {"GisMeteo":
                               {"Moscow": 'https://www.gismeteo.ru/weather-moscow-4368/10-days/',
                                "Krasnodar": 'https://www.gismeteo.ru/weather-krasnodar-5136/10-days/',
                                "Ekaterinburg": 'https://www.gismeteo.ru/weather-yekaterinburg-4517/10-days/'},
                           "Yandex":
                               {"Moscow": 'https://yandex.ru/weather/moscow?lat=55.755863&lon=37.6177',
                                "Krasnodar": 'https://yandex.ru/weather?lat=45.03546906&lon=38.97531128',
                                "Ekaterinburg": 'https://yandex.ru/weather?lat=56.8380127&lon=60.59747314'}}

        self.datasets = {
            "Moscow": {
                "GisMeteo": pd.read_csv(os.path.join(os.path.join('data'), 'Moscow_GisMeteo_10.csv'), sep=',',
                                    index_col='date'),
                "Yandex": pd.read_csv(os.path.join(os.path.join('data'), 'Moscow_Yandex_10.csv'), sep=',',
                                  index_col='date')},
            "Krasnodar": {
                "GisMeteo": pd.read_csv(os.path.join(os.path.join('data'), 'Krasnodar_GisMeteo_10.csv'), sep=',',
                                        index_col='date'),
                "Yandex": pd.read_csv(os.path.join(os.path.join('data'), 'Krasnodar_Yandex_10.csv'), sep=',',
                                      index_col='date')},
            "Ekaterinburg": {
                "GisMeteo": pd.read_csv(os.path.join(os.path.join('data'), 'Ekaterinburg_GisMeteo_10.csv'), sep=',',
                                        index_col='date'),
                "Yandex": pd.read_csv(os.path.join(os.path.join('data'), 'Ekaterinburg_Yandex_10.csv'), sep=',',
                                      index_col='date')}}

    def get_weather_forecast_Yandex(self, city, type):
        city_url = self.cities_url[type][city]

        headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )
        response = requests.get(city_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        temp_max = soup.find_all('div', class_='temp forecast-briefly__temp forecast-briefly__temp_day')
        temp_min = soup.find_all('div', class_='temp forecast-briefly__temp forecast-briefly__temp_night')
        weather = soup.find_all('div', class_='forecast-briefly__condition')

        forecast_data = []

        for i in range(1, 11):
            max_temp = temp_max[i].find('span', class_='temp__value temp__value_with-unit').get_text(strip=True)
            min_temp = temp_min[i].find('span', class_='temp__value temp__value_with-unit').get_text(strip=True)
            weather_today = weather[i].get_text(strip=True)

            forecast_data.append({
                'max_temp': max_temp,
                'min_temp': min_temp,
                'weather': weather_today
            })

        return forecast_data

    def get_weather_forecast_GisMeteo(self, city, type):
        city_url = self.cities_url[type][city]

        headers = requests.utils.default_headers()

        headers.update(
            {
                'User-Agent': 'My User Agent 1.0',
            }
        )
        response = requests.get(city_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        temp_max = soup.find_all('div', class_='maxt')
        temp_min = soup.find_all('div', class_='mint')
        weather = soup.find_all('div', class_='row-item')

        forecast_data = []

        for i in range(10):
            max_temp = temp_max[i].find('span', class_='unit unit_temperature_c').get_text(strip=True)
            min_temp = temp_min[i].find('span', class_='unit unit_temperature_c').get_text(strip=True)
            weather_today = weather[i].find('div', class_='weather-icon tooltip').get('data-text', '')

            forecast_data.append({
                'max_temp': max_temp,
                'min_temp': min_temp,
                'weather': weather_today
            })

        return forecast_data

    def create_today(self, city, type, today=datetime.now().strftime('%Y-%m-%d')):
        if type == "Yandex":
            forecast_data = self.get_weather_forecast_Yandex(city, type)
        elif type == "GisMeteo":
            forecast_data = self.get_weather_forecast_GisMeteo(city, type)
        else:
            raise "TypeError"

        max_temps = [data['max_temp'] for data in forecast_data]
        min_temps = [data['min_temp'] for data in forecast_data]
        weather = [data['weather'] for data in forecast_data]

        data = {'date': [today]}

        for i in range(10):
            data[f'day{i + 1}'] = [int(max_temps[i]) if max_temps[i][0] != '-' else int(max_temps[i]) * (-1)]

        for i in range(10):
            data[f'night{i + 1}'] = [int(min_temps[i]) if min_temps[i][0] != '-' else int(min_temps[i]) * (-1)]

        for i in range(10):
            data[f'weather{i + 1}'] = [weather[i] if i < len(weather) else None]

        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)

        return df

    def update(self, city, type):
        try:
            df_new = self.create_today(city, type)
            self.datasets[city][type] = pd.concat([self.datasets[city][type], df_new])

            self.datasets[city][type].to_csv(os.path.join(os.path.join('data'), f'{city}_{type}_10.csv'))
            self.datasets[city][type].to_excel(os.path.join(os.path.join('data'), f'{city}_{type}_10.xlsx'))
            print("GOOD!")
        except:
            print("ERROR!")

    def create_new_day(self, city, type, date):
        date = datetime.strptime(date, '%Y-%m-%d').strftime("%Y-%m-%d")

        data = {'date': [date]}

        for i in range(10):
            print(f"\nВведите day{i + 1}:\n")
            input_day = input()
            data[f'day{i + 1}'] = int(input_day)

        for i in range(10):
            print(f"\nВведите night{i + 1}:\n")
            input_night = input()
            data[f'night{i + 1}'] = int(input_night)

        for i in range(10):
            print(f"\nВведите weather{i + 1}:\n")
            input_weather = input()
            data[f'weather{i + 1}'] = input_weather

        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)

        try:
            self.datasets[city][type] = pd.concat([self.datasets[city][type], df]).sort_index()

            self.datasets[city][type].to_csv(os.path.join(os.path.join('data'), f'{city}_{type}_10.csv'))
            self.datasets[city][type].to_excel(os.path.join(os.path.join('data'), f'{city}_{type}_10.xlsx'))
            print("GOOD!")
        except:
            print("ERROR!")

    def backup(self):
        csv_folder = os.path.join('backup')

        try:
            for city in self.datasets:
                for type in self.datasets[city]:
                    file_name_csv = f'{city}_{type}_10.csv'
                    file_path_csv = os.path.join(csv_folder, file_name_csv)

                    file_name_excel = f'{city}_{type}_10.xlsx'
                    file_path_excel = os.path.join(csv_folder, file_name_excel)

                    self.datasets[city][type].to_csv(file_path_csv)
                    self.datasets[city][type].to_excel(file_path_excel)
            print("GOOD backup!")
        except:
            print("ERROR backup!")

    def view(self, city, type, key="tail"):
        if key == "tail":
            return self.datasets[city][type].tail()
        elif key == "head":
            return self.datasets[city][type].head()
        elif key == "all":
            return self.datasets[city][type]
        else:
            raise KeyError