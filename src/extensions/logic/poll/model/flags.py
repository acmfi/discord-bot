import re
from src.extensions.logic.lib.flags import FlagsCommand
from src.extensions.logic.exceptions.exceptions import InvalidFlagException
from src.extensions.logic.poll.default_values import DEFAULT_DURATION


class PollFlagsCommand(FlagsCommand):
    """Flags for the poll command. 

    It creates a flag with the attributes of the FlagsCommand class. Valid flags can be seen in the parameter _FLAGS

    Attributes:
        value (Message): any: The value of the flag. Depending on the flag:
            * --time: It will return a integer  
    """

    """
    This are the flags for the poll. The user will use --FLAG in order to use it. These options are:
        - time: It will allow the user specify the time. If user don't use it, the default value will be used
                It needs a value which will be a number follower by one othe following letters: s, m, h, d
        - no-time: It will allow the user to create a poll indefinitely
    """
    _FLAGS = {
        "time": {
            "needs_value": True,
            "description": "Time the users have for voting. Expects a positive integer that represents "
                           "seconds(s), minutes(m), hours(h) or days(d).",
            "examples": ['/poll --time 10m "Only 10 minutes poll"', '/poll --time 2h "2 hours poll"'],
            "default_value": DEFAULT_DURATION
        },
        "no-time": {
            "needs_value": False,
            "description": "If you want to create your poll for a uncertain amount of time",
            "examples": []
        }
    }

    def __init__(self, needs_value, argument, description, examples, value_input, default_value=None):
        """
        It will use the constructor of the parent and then it will set the value to an attribute if needed. 

        Args:
            needs_value (boolean): A flag might have a value, otherwise it will be a boolean (active-true/deactivated-false)
            argument (string): It is the name of the flag it self 
            description (string): A small description of the flag. Only needed for the documentation for 
                                the user in how to use the command which the flag is part of
            examples (string[]): An array of string containing examples. Only needed for the documentation for 
                                the user in how to use the command which the flag is part of
            value_input (any): If the flag needs a value, this is the value given by the user
            default_value (any): If the flag needs a value and the user did not use the flag, then the code
                                will set a value by default.
        """
        super().__init__(needs_value, argument, description,
                         examples, value_input, default_value)
        self.value = self.parse_flag_value(self.argument, self.value_input)

    def parse_flag_value(self, argument, value_input):
        """
        If the flag needs a value, it will parse the value and set it in the correct way. 
        Flags with value:
            * --time: it will convert it to seconds the value given by the user.
                      Example 1m will return 60. 1d will return 86400

        Args:
            argument (string): It is the name of the flag it self 
            value_input (any): If the flag needs a value, this is the value given by the user or the value by default

        Returns:
            any: The value of the flag. Depending on the flag:
                * --time: It will return a integer

        Raises:
            InvalidFlagException: If the value is not a number followed by s|m|h|d
        """
        if argument == "time":
            regex = r"^(\d*)([s|m|h|d])$"
            matches = re.findall(regex, value_input)
            if len(matches) != 1 or len(matches[0]) != 2 and matches[0][1] not in ["s", "m", "h", "d"]:
                raise InvalidFlagException
            amount, time_type = matches[0]
            if time_type == "s":
                return int(amount)
            elif time_type == "m":
                return int(amount) * 60
            elif time_type == "h":
                return int(amount) * 60 * 60
            elif time_type == "d":
                return int(amount) * 60 * 60 * 24
