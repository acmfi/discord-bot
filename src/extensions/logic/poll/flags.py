import re
from src.extensions.logic.lib.flags import FlagsCommand
from src.extensions.logic.exceptions.exceptions import InvalidFlagException
from src.extensions.logic.poll.default_values import DEFAULT_DURATION


class PollFlagsCommand(FlagsCommand):
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
        super().__init__(needs_value, argument, description,
                         examples, value_input, default_value)
        self.value = self.parse_flag_value(self.argument, self.value_input)

    def parse_flag_value(self, argument, value_input):
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
