import getopt

from src.extensions.logic.exceptions.exceptions import InvalidFlagException, InvalidInputException
from src.extensions.logic.lib.command import Command
from src.extensions.logic.poll.flags import PollFlagsCommand
from src.extensions.logic.poll.multiple_option import MultipleOptionPollModel
from src.extensions.logic.poll.yesorno import YesOrNoPollModel


class PollCommand(Command):
    description = 'Creates a multiple option poll or yes/no question. The users will vote one or more options for a ' \
                  'certain amount of time. Multiple options poll need at least 2 options, and yes/no polls' \
                  'don\'t need options at all'

    def get_description(self):
        return self.description

    def get_usage(self):
        usage = '[FLAGS] "Question" ["Option 1" ... "Option N]"\n'
        flags_str = ""
        flags = PollFlagsCommand._FLAGS
        length = max([len(a) for a in flags]) + 5
        for k, v in flags.items():
            command = f"--{k}".ljust(length)
            example = f"\n\t{' ' * len(command)}{' | '.join(v['examples'])}" if "examples" in v else ""
            flags_str += f"\t{command}{v['description']}{example}\n"
        help_str = f"\t{'--help'.ljust(length)}Shows this help\n"
        return usage + flags_str + help_str

    def parser(self, input_args, ctx):
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
            return YesOrNoPollModel(ctx.message, args[0], user_flags), None
        else:
            return MultipleOptionPollModel(ctx.message, args[0], args[1:], user_flags), None
