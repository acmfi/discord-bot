import re
from discord.ext import commands
from discord.utils import get

def setup(bot):
    bot.add_cog(Poll(bot))


class PollModel:
    emojis = {
        "short": [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:",
                  ":keycap_ten:"],
        "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(1, 10)]
    }

    def __init__(self, question=None, options=None):
        if question is None or options is None:
            return
        self.question = question
        self.options = options

    def from_message(self, message):
        self.message = message
        self.question, self.options = self.poll_parser(self.message.clean_content)
        self.set_poll_str()
        return self

    def poll_parser(self, msg):
        regex = r"\"(.+?)\""
        matches = list(re.finditer(regex, msg, re.MULTILINE))
        if len(matches) < 3 or len(matches) > 11 or matches[-1].end() != len(msg):
            raise Exception('Bro, lo has puesto mal. Si quieres un ejemplo mira cruck.\n\n\t'
                            '/poll "Aquí tu pregunta" "Una opción" "Como mínimo 2 opciones" '
                            '"Hasta 10 opciones, que guay!"')
        return matches[0].group(1), [m.group(1) for m in matches[1:]]

    def set_poll_str(self):
        question = f"**{self.question}**"
        options = "\n".join([f"{self.emojis['short'][i]}{' '*3}{o}" for i, o in enumerate(self.options)])
        self.reactions = {
            "short": self.emojis["short"][:len(self.options)],
            "unicode": self.emojis["unicode"][:len(self.options)]
        }
        self.poll_str = f"{question}\n\n{options}"

    def __str__(self):
        options_str = " ".join(['"{}"'.format(o) for o in self.options])
        return '/poll "{0}" {1}'.format(self.question, options_str)

    def __eq__(self, other):
        if isinstance(other, PollModel):
            return self.question == other.question and self.options == other.options



class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description='Creates a poll and the participants will vote one or more options',
                      usage='"Question" "Option 1" ... "Option N"')
    async def create_poll(self, ctx):
        try:
            poll_model = PollModel().from_message(ctx.message)
            print(f"Log: New poll. Question: {poll_model.question}. Options: {poll_model.options}")
        except Exception as e:
            await ctx.message.channel.send(f"```{e}```")
            print(f"Log: Invalid input {ctx.message.clean_content} || {e}")
            return

        poll_sent = await ctx.message.channel.send(poll_model.poll_str)
        [await poll_sent.add_reaction(reaction) for reaction in poll_model.reactions["unicode"]]