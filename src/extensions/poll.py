import re
from discord.ext import commands


def setup(bot):
    bot.add_cog(Poll(bot))


EMOJIS = {
    "short": [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:",
              ":keycap_ten:"],
    "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, 11)]
}


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
    def __init__(self, message, question):
        self.message = message
        self.question = question
        self.poll_str = ""

    def set_poll_str(self):
        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[str(o) for o in self.options]}"

    def __str__(self):
        return self.poll_str


class MultipleOptionPollModel(PollModel):
    def __init__(self, message, question, options):
        super().__init__(message, question)
        self.options = [PollOption(o).set_keycap_emoji(i) for i, o in enumerate(options, start=1)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


class YesOrNoPollModel(PollModel):
    def __init__(self, message, question):
        super().__init__(message, question)
        options = ["True", "False"]
        emojis = ["tick", "cross"]
        self.options = [PollOption(o).set_yesno_emoji(e) for o, e in zip(options, emojis)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, YesOrNoPollModel):
            return self.question == other.question \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


def _poll_parser(message):
    message_content = message.clean_content
    regex = r"\"(.+?)\""
    matches = list(re.finditer(regex, message_content, re.MULTILINE))
    if (len(matches) < 3 or len(matches) > 11 or matches[-1].end() != len(message_content)) and len(matches) != 1:
        raise Exception('Bro, lo has puesto mal. Si quieres un ejemplo mira cruck.\n\n\t'
                        '/poll "Aquí tu pregunta" "Una opción" "Como mínimo 2 opciones" '
                        '"Hasta 10 opciones, que guay!"')
    if len(matches) != 1:
        return MultipleOptionPollModel(message, matches[0].group(1), [m.group(1) for m in matches[1:]])
    else:
        return YesOrNoPollModel(message, matches[0].group(1))


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description='Creates a poll and the participants will vote one or more options',
                      usage='"Question" "Option 1" ... "Option N"')
    async def create_poll(self, ctx):
        try:
            poll_model = _poll_parser(ctx.message)
            print(poll_model.get_log())
        except Exception as e:
            await ctx.message.channel.send(f"```{e}```")
            print(f"Log: Invalid input {ctx.message.clean_content} || {e}")
            return

        # Send the poll
        poll_sent = await ctx.message.channel.send(poll_model.poll_str)

        # React with emojis, each emoji is related to an option
        [await poll_sent.add_reaction(option.emoji.unicode) for option in poll_model.options]
