from discord.ext import commands
from src.extensions.logic.exceptions.exceptions import InvalidInputException, InvalidFlagException


def setup(bot):
    bot.add_cog(Poll(bot))


class FlagsCommand:
    """Flags for the command. 

    It creates a flag. Flags are a way to set options and pass in arguments to the commands you run.
    For the shake of simplicity, this proyect will only use long flags with -- grammar.

    Attributes:
        needs_value (boolean):  A flag might have a value, otherwise it will be a boolean (active-true/deactivated-false)
        argument (string):      It is the name of the flag it self 
        description (string):   A small description of the flag. Only needed for the documentation for 
                                the user in how to use the command which the flag is part of
        examples (string[]):    An array of string containing examples. Only needed for the documentation for 
                                the user in how to use the command which the flag is part of
        value_input (any):      If the flag needs a value, this is the value given by the user
        default_value (any):    If the flag needs a value and the user did not use the flag, then the code
                                will set a value by default.
    """

    def __init__(self, needs_value, argument, description, examples, value_input, default_value=None):
        """
        Args:
            needs_value (boolean):  A flag might have a value, otherwise it will be a boolean (active-true/deactivated-false)
            argument (string):      It is the name of the flag it self 
            description (string):   A small description of the flag. Only needed for the documentation for 
                                    the user in how to use the command which the flag is part of
            examples (string[]):    An array of string containing examples. Only needed for the documentation for 
                                    the user in how to use the command which the flag is part of
            value_input (any):      If the flag needs a value, this is the value given by the user
            default_value (any):    If the flag needs a value and the user did not use the flag, then the code
                                    will set a value by default.

        Raises:
            InvalidFlagException: if the flag needs a value and both value_input and default_value are None
        """
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
        """
        Creates a string for printing purposes containing the flag most important information.
        If the flag needs a value, it will be printed as well

        Returns:
            str: The flag in string format
        """
        flag_str = f"--{self.argument}"
        if self.needs_value:
            flag_str = f"{flag_str} {self.value_input}"
        return flag_str

    def __eq__(self, other):
        """
        Compare if `other` contains the same values as `self`

        Args:
            other (FlagsCommand): Object which the self object will be compared to.

        Returns:
            boolean: True if both objects contain the same values. False otherwise.
        """
        if isinstance(other, FlagsCommand):
            if self.argument == other.argument:
                if self.needs_value and other.needs_value:
                    return other.value is not None and other.value == self.value
                else:
                    return True
