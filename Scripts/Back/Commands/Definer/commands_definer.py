from Scripts.Back.Commands.Objects import command_objects

import Scripts.Back.Commands.Definer.Utils.utils as utils

commands_dict = {
    'greeting': command_objects.GreetingCommand(),
    'launch': command_objects.LaunchCommand(),
    'time': command_objects.TimeCommand(),
    'weather': command_objects.WeatherCommand(),
    'sleep': command_objects.SleepCommand(),
    'journal': command_objects.JournalCommand(),
    'shutdown': command_objects.ShutDownCommand(),
    'minimize': command_objects.MinimizeCommand()
}

paths_dict = {
    'games': ['игра', 'игру', 'запустить игру'],
    'progs': ['прога', 'прогу', 'запустить прогу', 'запусти'],
}


def get_command_object(key: str, command: str):
    object = commands_dict[key]

    if object.requires_path:
        result = utils.is_similar_string_in_dictionary(paths_dict, command, 0.8)
        if result[0]:
            object.set_path(result[1])

    if object.requires_command:
        object.set_command(command)

    return object
