from Scripts.Back.Commands.Objects.Journal.journal import Journal
from Scripts.Back.Commands.Objects.Parsers.commands_parser import get_journal_command, get_minimize_command
from Scripts.Back.Commands.Objects.Processors.windows_processor import min_max
from Scripts.Back.Commands.Objects.Speaker.speaker import speak
from _datetime import datetime
from Scripts.Utils.events_handler import dispatch_event
from ctypes import windll, byref, Structure, WinError, POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HMONITOR, HDC, RECT, LPARAM, DWORD, BYTE, WCHAR, HANDLE

import abc
import random
import os
import requests
import pymorphy3


class Command(abc.ABC):
    requires_path = False
    requires_command = False

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
        self.requires_path = True
        self.requires_command = True

    def set_command(self, command: str):
        self.app = command

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

            city = self.morph.parse(self.city)[0].inflect({'datv'}).word
            gradus = self.morph.parse('градус')[0]
            weather = res['weather'][0]['description']
            temp = round(res['main']['temp'])
            min_temp = round(res['main']['temp_min'])
            max_temp = round(res['main']['temp_max'])
            temp_gradus = gradus.make_agree_with_number(temp).word

            phrase = f'На улице в {city} {weather}. Температура: {temp} {temp_gradus}'

            if min_temp == max_temp:
                phrase = f'{phrase} и не изменится.'
            else:
                min_temp_gradus = gradus.make_agree_with_number(min_temp).word
                max_temp_gradus = gradus.make_agree_with_number(max_temp).word
                phrase = f'{phrase}. Меняется от {min_temp} {min_temp_gradus} до {max_temp} {max_temp_gradus}.'

            speak(phrase)

        except requests.exceptions.ReadTimeout:
            speak('Не получилось узнать погоду')
        except requests.exceptions.ConnectTimeout:
            speak('Не получилось достучаться до погодных богов')


class JournalCommand(Command):
    def __init__(self):
        self.requires_command = True
        self.journal = Journal()
        self.command = str

    def set_command(self, command: str):
        self.command = command

    def execute(self):
        command = get_journal_command(self.command)

        self.journal.add(**command)


class SleepCommand(Command):
    def execute(self):
        dispatch_event('stop_recognition')


class ShutDownCommand(Command):
    _MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, POINTER(RECT), LPARAM)

    class _PHYSICAL_MONITOR(Structure):
        _fields_ = [
            ('handle', HANDLE),
            ('description', WCHAR * 128)
        ]

    def execute(self):
        def iterate_physical_monitors(close_handles=True):
            def callback(hmonitor, hdc, lprect, lparam):
                monitors.append(HMONITOR(hmonitor))
                return True

            monitors = []
            if not windll.user32.EnumDisplayMonitors(None, None, self._MONITORENUMPROC(callback), None):
                raise WinError('EnumDisplayMonitors failed')

            for monitor in monitors:
                count = DWORD()
                if not windll.dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(monitor, byref(count)):
                    raise WinError()
                physical_array = (self._PHYSICAL_MONITOR * count.value)()
                if not windll.dxva2.GetPhysicalMonitorsFromHMONITOR(monitor, count.value, physical_array):
                    raise WinError()
                for physical in physical_array:
                    yield physical.handle
                    if close_handles:
                        if not windll.dxva2.DestroyPhysicalMonitor(physical.handle):
                            raise WinError()

        def set_vcp_feature(monitor, code, value):
            if not windll.dxva2.SetVCPFeature(HANDLE(monitor), BYTE(code), DWORD(value)):
                raise WinError()

        for handle in iterate_physical_monitors():
            set_vcp_feature(handle, 0xd6, 0x04)

        windll.powrprof.SetSuspendState(False, True, False)


class MinimizeCommand(Command):
    def __init__(self):
        self.requires_command = True
        self.command = ''

    def set_command(self, command: str):
        self.command = command

    def execute(self):
        app = get_minimize_command(self.command)

        min_max(True, app)
