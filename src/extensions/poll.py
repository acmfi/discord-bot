import re
from discord.ext import commands
import getopt
import time
import rx
from rx import operators as op
import asyncio


def setup(bot):
    bot.add_cog(Poll(bot))


EMOJIS = {
    "short": [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"],
    "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, 10)]
}

CLOCKS_EMOJI = [f":clock{hour}:" for hour in range(1, 13)]

DEFAULT_DURATION = "1d"

# Seconds for a period. Each period will update the discord message containing the poll and point show
# how much time left
REFRESH_RATE = 5


class InvalidInputException(Exception):
    pass


class InvalidFlagException(Exception):
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
    def __init__(self, user_message, question, flags):
        # Original message with the command which invoke the poll to be created
        self.user_message = user_message

        # Question of the poll
        self.question = question

        # Different answers
        self.options = []

        # Flags used in the command by the invoker
        self.flags = flags

        # String containing the poll which will be sent to the users in the channel
        self.poll_str = ""

        # Object created by the Discord library containing the poll. The value will be set after
        # we send the message with the poll
        self.bot_message = None

        self.created_at = time.time()

        time_flag = list(filter(lambda flag: flag.argument == "time", self.flags))
        if len(time_flag) == 0:
            no_time_flag = list(filter(lambda flag: flag.argument == "no-time", self.flags))
            if len(no_time_flag) == 0:
                self.duration = parse_flag_value("time", DEFAULT_DURATION)
            else:
                self.duration = -1
        else:
            self.duration = time_flag[0].value

    def set_poll_str(self):
        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[o.option_str for o in self.options]}"

    def __str__(self):
        return self.poll_str

    def get_reaction_emojis(self):
        # Returns the emojis in a lists
        return [option.emoji.unicode for option in self.options]


class MultipleOptionPollModel(PollModel):
    def __init__(self, user_message, question, options, flags=None):
        super().__init__(user_message, question, flags)
        self.options = [PollOption(o).set_keycap_emoji(i) for i, o in enumerate(options, start=1)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question and self.flags == other.flags and self.poll_str == other.poll_str \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


class YesOrNoPollModel(PollModel):
    def __init__(self, user_message, question, flags=None):
        super().__init__(user_message, question, flags)
        options = ["True", "False"]
        emojis = ["tick", "cross"]
        self.options = [PollOption(o).set_yesno_emoji(e) for o, e in zip(options, emojis)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, YesOrNoPollModel):
            return self.question == other.question and self.flags == other.flags \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


class FlagsPollCommand:
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
        self.value = parse_flag_value(self.argument, self.value_input)

    def __str__(self):
        flag_str = f"--{self.argument}"
        if self.needs_value:
            flag_str = f"{flag_str} {self.value_input}"
        return flag_str

    def __eq__(self, other):
        if isinstance(other, FlagsPollCommand):
            if self.argument == other.argument:
                if self.needs_value and other.needs_value:
                    return other.value is not None and other.value == self.value
                else:
                    return True


def seconds2str(seconds):
    n_days = int(seconds / (24 * 60 * 60))
    if n_days > 0:
        n_hours = int((seconds % (24 * 60 * 60)) / (60 * 60))
        if n_hours > 0:
            return f"{n_days}d y {n_hours}h"
        else:
            return f"{n_days}d"
    n_hours = int(seconds / (60 * 60))
    if n_hours > 0:
        n_minutes = int((seconds % (60 * 60)) / 60)
        if n_minutes > 0:
            return f"{n_hours}h y {n_minutes}m"
        else:
            return f"{n_hours}h"
    n_minutes = int(seconds / 60)
    if n_minutes > 0:
        n_seconds = seconds % 60
        if n_seconds > 0:
            return f"{n_minutes}m y {n_seconds}s"
        else:
            return f"{n_minutes}m"
    return f"{seconds}s"


def parse_flag_value(argument, value_input):
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

class PollHandler:
    def __init__(self, poll: PollModel):
        self.poll = poll

        self.ob = rx.interval(REFRESH_RATE)
        self.sub = self.ob.pipe(
            op.take_until_with_time(self.duration)  # Seconds that the poll will last
        )

        # Use for avoid waiting to edit message
        # https://stackoverflow.com/questions/53722398/how-to-send-a-message-with-discord-py-from-outside-the-event-loop-i-e-from-pyt
        self._loop = asyncio.get_event_loop()

    async def send_poll_n_react(self, ctx):
        # Send the poll
        self.poll.bot_message = await ctx.message.channel.send(str(self.poll))

        # React to the message with the different emojis associated to the options
        [await self.poll.bot_message.add_reaction(emoji) for emoji in self.poll.get_reaction_emojis()]

    async def subscribe(self):
        self.sub.subscribe(
            on_next=self.__on_next,
            on_error=lambda e: self.__on_error(e),
            on_completed=self.__on_completed
        )

    def __on_next(self, i):
        seconds_left = int(self.poll.created_at + self.poll.duration - time.time())
        seconds_left = 5 * round(seconds_left / 5)  # Round seconds to 0 or 5
        poll_str = f"{str(self.poll)}\n\n{CLOCKS_EMOJI[i % 12]}  La votación cierra en {seconds2str(seconds_left)}"
        self.__edit_msg(poll_str)

    def __on_error(self, iteration):
        pass

    def __on_completed(self):
        poll_str = f"{str(self.poll)}\n\n:male_dancer::dancer:  La votación ha terminado  :male_dancer::dancer:"
        self.__edit_msg(poll_str)

    def __edit_msg(self, msg):
        asyncio.run_coroutine_threadsafe(
            self.poll.bot_message.edit(content=msg), self._loop)


class PollManager:
    def __init__(self):
        self.current_polls = []

    async def add(self, ctx, poll):
        poll_handler = PollHandler(poll)
        await poll_handler.send_poll_n_react(ctx)
        await poll_handler.subscribe()
        self.current_polls.append(poll_handler)


class PollCommand:
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

    description = 'Creates a multiple option poll or yes/no question. The users will vote one or more options for a ' \
                  'certain amount of time. Multiple options poll need at least 2 options, and yes/no polls' \
                  'don\'t need options at all'

    def get_description(self):
        return self.description

    def get_usage(self):
        usage = '[FLAGS] "Question" ["Option 1" ... "Option N]"\n'
        flags = ""
        length = max([len(a) for a in self._FLAGS]) + 5
        for k, v in self._FLAGS.items():
            command = f"--{k}".ljust(length)
            example = f"\n\t{' ' * len(command)}{' | '.join(v['examples'])}" if "examples" in v else ""
            flags += f"\t{command}{v['description']}{example}\n"
        help_str = f"\t{'--help'.ljust(length)}Shows this help\n"
        return usage + flags + help_str

    def parser(self, input_args, ctx):
        if len(input_args) == 1 and input_args[0] == "/poll":
            raise InvalidInputException()

        try:
            flags_input, args = getopt.getopt(input_args, "",
                                              ["help"] + [f + "=" if self._FLAGS[f]["needs_value"] else f
                                                          for f in self._FLAGS])
        except getopt.GetoptError:
            raise InvalidFlagException()

        flags_name = [f[0] for f in flags_input]
        if "--help" in flags_name:
            raise InvalidInputException()
        if "--time" in flags_name and "--no-time" in flags_name:
            raise InvalidFlagException("Cannot use --time and --no-time at the same time")

        flags = []

        # Flags given by the user
        for (k, v) in flags_input:
            f = self._FLAGS[k[2:]]
            flags_name.append(k[2:])
            flags.append(FlagsPollCommand(f["needs_value"], k[2:], f["description"], f["examples"], v,
                                          f["default_value"] if "default_value" in f else None))
        if len(args) in [0, 2] or len(args[1:]) > 10:
            raise InvalidInputException()
        if len(args) == 1:
            return YesOrNoPollModel(ctx.message, args[0], flags)
        else:
            return MultipleOptionPollModel(ctx.message, args[0], args[1:], flags)


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_
        self.poll_manager = PollManager()

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description=PollCommand().get_description(), usage=PollCommand().get_usage())
    async def create_poll(self, ctx, *args):
        try:
            poll = PollCommand().parser(args, ctx)
            print(poll.get_log())
        except InvalidInputException as e:
            await ctx.message.channel.send(f"```{PollCommand().get_usage()}```")
            print(f"Log: Invalid input or help requested {ctx.message.clean_content} || {e}")
            return
        except InvalidFlagException as e:
            await ctx.message.channel.send(f"```{PollCommand().get_usage()}```")
            print(f"Log: Invalid flag in {ctx.message.clean_content} || {e}")
            return
        except Exception as e:
            await ctx.message.channel.send(f"```{PollCommand().get_usage()}```")
            print(f"Log: Invalid input or help requested {ctx.message.clean_content} || {e}")
            return

        await self.poll_manager.add(ctx, poll)
