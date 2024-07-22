import os
import pathlib
import json

from Scripts.Utils.events_handler import dispatch_event, register_handler


class JournalItem:
    id = int
    text = str
    date = str
    time = str
    completed = False

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.text = kwargs['text']
        self.date = kwargs['date']
        self.time = kwargs['time']

        if 'completed' in kwargs:
            self.completed = kwargs['completed']

    def get(self):
        data = {
            'id': self.id,
            'text': self.text,
            'date': self.date,
            'time': self.time,
            'completed': self.completed
        }

        return data


class Journal:
    path: str = 'LocalData\\journal'
    file_name: str = 'journal.json'
    file_path: str = None

    journal_items = []

    def __init__(self):
        self.validate_path()

        with open(self.file_path, 'r') as file:
            data = json.load(file)

            if data is dict:
                data = json.loads(json.load(file))

            for item in data["items"]:
                self.journal_items.append(JournalItem(**item))

            register_handler('to_do_list_requested', self.populate_list)

    def validate_path(self):
        path = pathlib.Path().cwd()

        while (not (path / self.path).exists()) or (not (path / 'Scripts').exists()):
            path = path.parent

        if (path / self.path).exists():
            self.file_path = os.path.join(path, self.path, self.file_name)
        else:
            path = os.path.join(path, self.path)
            os.mkdir(path)
            self.file_path = os.path.join(path, self.file_name)

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write('{\n"items": []\n}')

    def add(self, **kwargs):
        kwargs["id"] = len(self.journal_items)
        self.journal_items.append(JournalItem(**kwargs))

        dispatch_event('to_do_list_added', item=self.journal_items[-1])

        with open(self.file_path, 'w') as file:
            json_data = '{"items": ['

            for i in range(len(self.journal_items)):
                item = self.journal_items[i]
                dumps = json.dumps(item.get())
                json_data = f"{json_data} {dumps}"

                if i != len(self.journal_items) - 1:
                    json_data = f'{json_data},'

            json_data = json_data + ']}'
            json_data = json_data.replace("'", '"')
            json_data = json.loads(json_data)

            json.dump(json_data, file, indent=2)

    def get(self):
        if len(self.journal_items) == 0:
            with open(self.file_path, 'r') as file:
                data = json.load(file)

                for item in data["items"]:
                    self.journal_items.append(JournalItem(**item))

        return self.journal_items

    def populate_list(self):
        dispatch_event('to_do_list_populated', list=self.get())
