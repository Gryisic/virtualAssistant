from Scripts.Back.Commands.Objects.command_objects import Command

class CommandsBuilder:
    commands = []

    def clear(self):
        self.commands.clear()
        return self

    def append(self, command: Command):
        self.commands.append(command)
        return self

    def build(self):
        return self.commands