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
            return
        self.emoji = Emoji(EMOJIS["short"][index-1], EMOJIS["unicode"][index-1])
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


class MultipleOptionPollModel(PollModel):
    def __init__(self, message, question, options):
        super().__init__(message, question)
        self.options = [PollOption(o).set_keycap_emoji(i) for i, o in enumerate(options, start=1)]
        self.poll_str = ""
        self.set_poll_str()

    def set_poll_str(self):
        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: Multiple option poll. Question: {self.question}. Options: {self.options}"

    def __str__(self):
        return self.poll_str

    def __eq__(self, other):
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question \
                   and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]


def _poll_parser(message):
    message_content = message.clean_content
    regex = r"\"(.+?)\""
    matches = list(re.finditer(regex, message_content, re.MULTILINE))
    if (len(matches) < 3 or len(matches) > 11 or matches[-1].end() != len(message_content)) and len(matches) != 2:
        raise Exception('Bro, lo has puesto mal. Si quieres un ejemplo mira cruck.\n\n\t'
                        '/poll "Aquí tu pregunta" "Una opción" "Como mínimo 2 opciones" '
                        '"Hasta 10 opciones, que guay!"')
    if len(matches) != 2:
        return MultipleOptionPollModel(message, matches[0].group(1), [m.group(1) for m in matches[1:]])
    else:
        # TODO YesOrNoPoll
        pass


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description='Creates a poll and the participants will vote one or more options',
                      usage='"Question" "Option 1" ... "Option N"')
    async def create_poll(self, ctx):
        try:
            poll_model = _poll_parser(ctx.message)
            if poll_model is None:
                print("Not implemented yet")
                return
            print(poll_model.get_log())
        except Exception as e:
            await ctx.message.channel.send(f"```{e}```")
            print(f"Log: Invalid input {ctx.message.clean_content} || {e}")
            return

        poll_sent = await ctx.message.channel.send(poll_model.poll_str)
        [await poll_sent.add_reaction(option.emoji.unicode) for option in poll_model.options]
