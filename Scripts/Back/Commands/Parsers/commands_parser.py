from re import split

separators = " и | или "

def get_commands_list(full_command: str):
    commands = split(separators, full_command)

    return commands