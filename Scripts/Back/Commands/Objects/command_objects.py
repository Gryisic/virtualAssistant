from Scripts.Back.Commands.Objects.Speaker.speaker import speak
from _datetime import datetime

import abc
import random
import os

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