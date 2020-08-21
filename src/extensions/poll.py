import re
from discord.ext import commands


def setup(bot):
    bot.add_cog(Poll(bot))


class PollModel:
    def __init__(self, question, options):
        self.question = question
        self.options = options

    def __str__(self):
        options_str = " ".join(['"{}"'.format(o) for o in self.options])
        return '/poll "{0}" {1}'.format(self.question, options_str)

    def __eq__(self, other):
        if isinstance(other, PollModel):
            return self.question == other.question and self.options == other.options


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    def poll_parser(self, msg):
        regex = r"\"(.+?)\""
        matches = list(re.finditer(regex, msg, re.MULTILINE))
        if len(matches) < 3 or matches[-1].end() != len(msg):
            raise Exception('Bro, lo has puesto mal. Si quieres un ejemplo mira cruck.\n\n\t'
                            '/poll "Aquí tu pregunta" "Una opción" "Como mínimo 2 opciones" '
                            '"Hasta 9 opciones, que guay!"')
        return PollModel(matches[0].group(1), [m.group(1) for m in matches[1:]])

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description='Creates a poll and the participants will vote one or more options',
                      usage='"Question" "Option 1" ... "Option N"')
    async def create_poll(self, ctx):
        try:
            poll_model = self.poll_parser(ctx.message.clean_content)
        except Exception as e:
            await ctx.message.channel.send(f"```{e}```")

        print("A new poll\n\tquestion: {}\n\toptions: {}".format(poll_model.question, poll_model.options))
        await ctx.message.channel.send("A new poll\n\tquestion: {}\n\toptions: {}".format(poll_model.question, poll_model.options))