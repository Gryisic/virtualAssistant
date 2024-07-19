from Scripts.Back.Commands.Objects.Speaker.speaker import speak
from _datetime import datetime

import abc
import random
import os
import requests
import pymorphy3

from Scripts.Utils.events_handler import dispatch_event


class Command(abc.ABC):
    requiresPath = False
    requiresApp = False

    @abc.abstractmethod
    def execute(self):
        pass


class GreetingCommand(Command):
    greetings = ['привет', 'бот', 'хай', 'приветик']

    def execute(self):
        responses = ['Как ты?', 'Чем могу помочь?', 'Какой прекрасный день!']
        index = random.randint(0, len(responses) - 1)
        speak(f"Приветик! {responses[index]}")


class TimeCommand(Command):
    def execute(self):
        time = datetime.now().strftime('%X')
        speak(time)


class LaunchCommand(Command):
    paths_dict = {
        'games': r'C:\Users\Gryis\Desktop\Гамес',
        'progs': r'C:\Users\Gryis\Desktop\Проги'
    }

    app = str
    path = str

    def __init__(self):
        self.requiresPath = True
        self.requiresApp = True

    def set_app(self, app: str):
        self.app = app

    def set_path(self, path: str):
        self.path = self.paths_dict[path]

    def execute(self):
        for f in os.listdir(self.path):
            name = f.removesuffix('.lnk').removesuffix('.url').lower()
            if (name in self.app):
                os.startfile(self.path + "\\" + name)
                speak(f'Запускаю: {name}')
                break


class WeatherCommand(Command):
    api_key = 'c2e0682fecf51aee9ac853f5fcf0b3e0'
    city = 'Пермь'
    morph = pymorphy3.MorphAnalyzer(lang='ru')

    def execute(self):
        speak('Узнаю погоду')

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
            }

            coord = requests.get(
                f'http://api.openweathermap.org/geo/1.0/direct?q={self.city}&appid={self.api_key}',
                headers=headers
            )

            coord = coord.json()[0]

            lat = coord['lat']
            lon = coord['lon']

            res = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric&lang=ru",
                headers=headers
            )

            res = res.json()

            gradus = self.morph.parse('градус')[0]
            weather = res['weather'][0]['description']
            temp = round(res['main']['temp'])
            min_temp = round(res['main']['temp_min'])
            max_temp = round(res['main']['temp_max'])
            temp_gradus = gradus.make_agree_with_number(temp).word
            min_temp_gradus = gradus.make_agree_with_number(min_temp).word
            max_temp_gradus = gradus.make_agree_with_number(max_temp).word
            city = self.morph.parse(self.city)[0].inflect({'datv'}).word

            speak(
                f'На улице в {city} {weather}. Температура: {temp} {temp_gradus}. Меняется от {min_temp} {min_temp_gradus} до {max_temp} {max_temp_gradus}.')

        except requests.exceptions.ReadTimeout:
            speak('Не получилось узнать погоду')
        except requests.exceptions.ConnectTimeout:
            speak('Не получилось достучаться до погодных богов')


class SleepCommand(Command):
    def execute(self):
        dispatch_event('stop_recognition')
