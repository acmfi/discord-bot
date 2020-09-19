from discord.ext import commands
from src.extensions.logic.exceptions.exceptions import InvalidInputException, InvalidFlagException


def setup(bot):
    bot.add_cog(Poll(bot))


class FlagsCommand:
    def __init__(self, needs_value, argument, description, examples, value_input, default_value=None):
        self.needs_value = needs_value
        self.argument = argument
        self.description = description
        self.examples = examples
        if value_input is None and default_value is not None:
            self.value_input = default_value
        elif needs_value and value_input is None and default_value is None:
            raise InvalidFlagException
        else:
            self.value_input = value_input

    def __str__(self):
        flag_str = f"--{self.argument}"
        if self.needs_value:
            flag_str = f"{flag_str} {self.value_input}"
        return flag_str

    def __eq__(self, other):
        if isinstance(other, FlagsCommand):
            if self.argument == other.argument:
                if self.needs_value and other.needs_value:
                    return other.value is not None and other.value == self.value
                else:
                    return True
