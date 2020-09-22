class Command:
    prefix = "!"  # Se puede sacar directamente de bot con _prefix = self.bot.command_prefix

    def __init__(self, name, aliases, brief, description, usage=""):
        self.name = name
        self.aliases = aliases
        self.description = description
        self.usage = usage
        self.brief = brief

    def get_command_n_aliases(self):
        return [self.prefix + command for command in ([self.name] + self.aliases)]
