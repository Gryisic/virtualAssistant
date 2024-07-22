from re import split
from _datetime import datetime


def get_commands_list(full_command: str):
    separators = " и | или "
    commands = split(separators, full_command)

    return commands


def get_journal_command(full_command: str):
    date_and_time = datetime.now()
    separators = " журнал | запись | заметка "
    split_command = split(separators, full_command)
    text = ''

    for i in range(1, len(split_command)):
        text = f'{text} {split_command[i]}'

    command = {
        "text": text.strip(" "),
        "date": date_and_time.strftime('%d/%m/%y'),
        "time": date_and_time.strftime('%X')
    }

    return command
