import os
import pathlib
import json

from _datetime import datetime


class Journal:
    path = 'LocalData\\journal'
    file_name = 'journal.json'
    file_path = None

    def __init__(self):
        path = pathlib.Path().cwd()

        while not (path / self.path).exists():
            path = path.parent

        self.file_path = f'{path}\\{self.path}\\{self.file_name}'

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write('{\n\n}')

    def add(self, **kwargs):
        with open(self.file_path, 'w') as file:
            data = self.get()
            text = kwargs['text']
            date = kwargs['date']
            #json.dump(data, file, indent=2)
            print(type(data))

    def get(self):
        with open(self.file_path, 'r') as file:
            return json.load(file)


if __name__ == '__main__':
    journal = Journal()
    args = {
        'text': 'Hi',
        'date': datetime.now().strftime('%d/%m/%y')
    }
    #journal.add(**args)
