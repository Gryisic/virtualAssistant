from Scripts.Back.Commands.Parsers.commands_parser import get_commands_list
from Scripts.Back.Commands.Builders import commands_builder
from Scripts.Back.Commands.Definer import commands_definer

import Scripts.Back.Commands.Definer.Utils.utils as utils

commands_dict = {
    'command': {
        'greeting': ['привет', 'бот', 'хай', 'приветик'],
        'launch': ['открой', 'запусти'],
        'time': ['время', 'сколько времени', 'назови время']
    }
}

builder = commands_builder.CommandsBuilder()

def process(command: str):
    commands = get_commands_list(command)
    builder.clear()

    for split_command in commands:
        for k, v in commands_dict['command'].items():
            if utils.is_strings_similar(v, split_command, 0.8) or utils.is_string_in_list(v, split_command):
                builder.append(commands_definer.get_command_object(k, split_command))

    for com in builder.build():
        com.execute()