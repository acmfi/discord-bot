import re
from discord.ext import commands
import getopt
from discord import Message

def setup(bot):
    bot.add_cog(Poll(bot))


EMOJIS = {
    "short": [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"],
    "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, 10)]
}

class InvalidInputException(Exception):
    pass

class Emoji:
    def __init__(self, short, unicode):
        self.short = short
        self.unicode = unicode

    def __eq__(self, other):
        if isinstance(other, Emoji):
            return self.short == other.short and self.unicode == other.unicode


class PollOption:
    def __init__(self, option_str):
        self.option_str = option_str
        self.emoji = None

    def set_keycap_emoji(self, index):
        if index < 1 or index > 11:
            raise Exception(f"Invalid emoji index {index}. Only valid between 0 and 9")
        self.emoji = Emoji(EMOJIS["short"][index - 1], EMOJIS["unicode"][index - 1])
        return self

    def set_yesno_emoji(self, emoji_type):
        if emoji_type == "tick":
            self.emoji = Emoji(":white_check_mark:", '\U00002705')
        elif emoji_type == "cross":
            self.emoji = Emoji(":x:", '\U0000274c')
        return self

    def __str__(self):
        return f"{self.emoji.short}{' ' * 3}{self.option_str}"

    def __eq__(self, other):
        if isinstance(other, PollOption):
            return self.option_str == other.option_str and self.emoji == other.emoji


class PollModel:
    def __init__(self, message, question, flags):
        self.message = message
        self.question = question
        self.flags = flags
        self.options = []
        self.poll_str = ""

    def set_poll_str(self):
        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[o.option_str for o in self.options]}"

    def __str__(self):
        return self.poll_str


class MultipleOptionPollModel(PollModel):
    def __init__(self, message, question, options, flags=None):
        super().__init__(message, question, flags)
        self.options = [PollOption(o).set_keycap_emoji(i) for i, o in enumerate(options, start=1)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question and self.flags == other.flags \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


class YesOrNoPollModel(PollModel):
    def __init__(self, message, question, flags=None):
        super().__init__(message, question, flags)
        options = ["True", "False"]
        emojis = ["tick", "cross"]
        self.options = [PollOption(o).set_yesno_emoji(e) for o, e in zip(options, emojis)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, YesOrNoPollModel):
            return self.question == other.question and self.flags == other.flags  \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]

class FlagsPollCommand():
    def __init__(self, needs_value, argument, description, examples, value=None):
        self.needs_value = needs_value
        self.argument = argument
        self.description = description
        self.examples = examples
        self.value = value

    def parse_value(self):
        if self.argument == "time":
            regex = r"^(\d*)([s|m|h|d])$"
            matches = re.findall(regex, self.value)
            if len(matches) != 1 or len(matches[0]) != 2 and matches[0][1] not in ["s", "m", "h", "d"]:
                raise Exception
            amount, time = matches[0]
            if time == "s":
                self.value = time
            elif time == "m":
                self.value = time * 60
            elif time == "h":
                self.value = time * 60 * 60
            elif time == "d":
                self.value = time * 60 * 60 * 24


    def __eq__(self, other):
        if isinstance(other, FlagsPollCommand):
            if self.argument == other.argument:
                if self.needs_value and other.needs_value:
                    return other.value is not None and other.value == self.value
                else:
                    return True

class PollCommand():
    _FLAGS = {
        "time": {
            "needs_value": True,
            "description": "Time the users have for voting. Expects a positive integer that represents "
                           "seconds(s), minutes(m), hours(h) or days(d).",
            "examples": ['/poll --time 10m "Only 10 minutes poll"', '/poll --time 2h "2 hours poll"']
        },
        "no-time": {
            "needs_value": False,
            "description": "If you want to create your poll for a uncertain amount of time",
            "examples": []
        }
    }

    def get_description(self):
        return 'Creates a multiple option poll or yes/no question. The users will vote one or more options for a ' \
               'certain amount of time'

    def get_usage(self):
        usage = '[FLAGS] "Question" "Option 1" ... "Option N"\n'
        flags = ""
        length = max([len(a) for a in self._FLAGS]) + 5
        for k, v in self._FLAGS.items():
            command = f"--{k}".ljust(length)
            example = f"\n\t{' ' * len(command)}{' | '.join(v['examples'])}" if "examples" in v else ""
            flags += f"\t{command}{v['description']}{example}\n"
        help = f"\t{'--help'.ljust(length)}Shows this help\n"
        return usage + flags + help

    def parser(self, input_args, ctx):
        try:
            flags_input, args = getopt.getopt(input_args, "",
                                              ["help"] + [f + "=" if self._FLAGS[f]["needs_value"] else f
                                                          for f in self._FLAGS])
        except getopt.GetoptError:
            raise InvalidInputException()
        if "--help" in [f[0] for f in flags_input]:
            raise InvalidInputException()

        flags = []
        for (k, v) in flags_input:
            f = self._FLAGS[k[2:]]
            flags.append(FlagsPollCommand(f["needs_value"], k[2:], f["description"], f["examples"], v))

        if len(args) in [0, 2]:
            raise InvalidInputException()
        if len(args) == 1:
            return YesOrNoPollModel(ctx.message, args[0], flags)
        else:
            return MultipleOptionPollModel(ctx.message, args[0], args[1:], flags)


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description=PollCommand().get_description(),usage=PollCommand().get_usage())
    async def create_poll(self, ctx, *args):
        print("Arguments", args)
        try:
            poll_model = PollCommand().parser(args, ctx)
            print(poll_model.get_log())
        except Exception as e:
            await ctx.message.channel.send(f"```{PollCommand().get_usage()}```")
            print(f"Log: Invalid input or help requested {ctx.message.clean_content} || {e}")
            return

        # Send the poll
        poll_sent = await ctx.message.channel.send(poll_model.poll_str)

        # React with emojis, each emoji is related to an option
        [await poll_sent.add_reaction(option.emoji.unicode) for option in poll_model.options]
        print("Sended")
