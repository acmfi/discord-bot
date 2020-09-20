import getopt

from src.extensions.logic.exceptions.exceptions import InvalidFlagException, InvalidInputException
from src.extensions.logic.lib.command import Command
from src.extensions.logic.poll.flags import PollFlagsCommand
from src.extensions.logic.poll.multiple_option import MultipleOptionPollModel
from src.extensions.logic.poll.yesorno import YesOrNoPollModel


class PollCommand(Command):
    """Command class for poll command. It is inherited from Command

    It creates a poll command object with the information and methods that will show to the user
    useful information about the command

    Attributes:
        description(string): String containing what the command does.
    """

    description = 'Creates a multiple option poll or yes/no question. The users will vote one or more options for a ' \
                  'certain amount of time. Multiple options poll need at least 2 options, and yes/no polls' \
                  'don\'t need options at all'

    def get_description(self):
        """
        It returns the description of the poll command

        Returns:
            string: String containing what the command does.
        """
        return self.description

    def get_usage(self):
        """
        It returns the usage of the poll command. The string returned will be the one sent by the bot to the user 
        when this execute the command with --help or puts an invalid input or flag.

        It will contain the description, grammar, flags with description and examples

        Returns:
            string: String containing how to use the command
        """

        usage = '[FLAGS] "Question" ["Option 1" ... "Option N]"\n'
        command_help = f"{self.get_description()}\n\nUSAGE:\n{usage}"
        flags_str = ""
        flags = PollFlagsCommand._FLAGS
        length = max([len(a) for a in flags]) + 5
        for k, v in flags.items():
            command = f"--{k}".ljust(length)
            example = f"\n\t{' ' * len(command)}{' | '.join(v['examples'])}" if "examples" in v else ""
            flags_str += f"\t{command}{v['description']}{example}\n"
        help_str = f"\t{'--help'.ljust(length)}Shows this help\n"
        return command_help + flags_str + help_str

    def parser(self, input_args, message):
        """
        Given the input_args, it will create the appropriate PollModel. If the poll contains more than two options, 
        then it will create a MultipleOptionPollModel. If the options are empty, then it will create a YesOrNoPollModel.
        If the options for the poll are other, a InvalidInputException will be raised. The library getopt will be used
        for parsing the flags.
        An example of empty options array would be: /poll --time 10m "Is JS the best language"
        An example of options array filled would be: /poll --time 10m "Is JS the best language" "Yes" "No" "I don't know JS"


        Args:
            input_args (string[]):  Array with the content given by the user. As example:
                                        User inputs: /poll --time 10m "Is JS the best language" (In this case options are empty)
                                        input_args will contain:
                                        input_args = ["/poll", "--time", "10m", "Is JS the best language"]
            message (Message):      A discord class for the messages containing the original message 
        Returns:
            PollModel: A poll model object
        """

        flags = PollFlagsCommand._FLAGS

        if len(input_args) == 1 and input_args[0] == "/poll":
            raise InvalidInputException()

        try:
            flags_input, args = getopt.getopt(input_args, "",
                                              ["help"] + [f + "=" if flags[f]["needs_value"] else f
                                                          for f in flags])
        except getopt.GetoptError:
            raise InvalidFlagException()

        flags_name = [f[0] for f in flags_input]
        if "--help" in flags_name:
            return None, True
        if "--time" in flags_name and "--no-time" in flags_name:
            raise InvalidFlagException(
                "Cannot use --time and --no-time at the same time")

        # Flags given by the user
        user_flags = []
        for (k, v) in flags_input:
            f = flags[k[2:]]
            flags_name.append(k[2:])
            user_flags.append(PollFlagsCommand(f["needs_value"], k[2:], f["description"], f["examples"], v,
                                               f["default_value"] if "default_value" in f else None))

        if len(args) in [0, 2] or len(args[1:]) > 10:
            raise InvalidInputException()
        if len(args) == 1:
            return YesOrNoPollModel(message, args[0], user_flags), None
        else:
            return MultipleOptionPollModel(message, args[0], args[1:], user_flags), None
