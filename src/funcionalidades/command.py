class Command:
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

    def get_command_n_aliases(self):
        return [self._prefix + command for command in ([self.name] + self.alias)]
