from discord.ext import commands
from discord import user

from src.Extensions.logic.ban_hammer import BanHammer
from src.Extensions.logic.lib.command import Command


def setup(bot):
    bot.add_cog(BanHammerView(bot))


class BanHammerView(commands.Cog):
    censor_command = Command(name="censor", aliases=["censura", "censurar", "ban"],
                             description="Añadir una palabra a la lista de palabras prohibidas",
                             usage="palabra_a_censurar", brief="Censurar una palabra")

    uncensor_command = Command(name="uncensor", aliases=["descensurar", "descensura", "unban"],
                               description="Quitar una palabra de la lista de palabras censuradas ",
                               usage="palabra_a_descensurar", brief="desCensurar una palabra")

    def __init__(self, bot):
        self.bot = bot
        self.hammer = BanHammer()

    @commands.command(name=censor_command.name, aliases=censor_command.aliases, brief=censor_command.brief,
                      description=censor_command.description, usage=censor_command.usage)
    @commands.has_role('Junta')
    async def ban_word(self, ctx):
        await ctx.send(self.hammer.add_word_blacklist(ctx.message))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return None

        if type(message.author) is user.User:  # Está interactuando con el bot, no en el canal general
            return None

        forbidden_words_used = self.hammer.get_forbidden_words(message=message,
                                                               commands_name=self.censor_command.get_command_n_aliases())
        if forbidden_words_used:
            # Delete the message
            await message.delete()
            # Send an alert through the channel
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")
            # Send a private message to the user        
            await message.author.send("El mensaje {} no se ajusta a las normas, intenta no usar {} ni parecidos"
                                      .format(str(f'```diff\n- "{message.content}"```'),
                                              str(forbidden_words_used).strip('[]')))

    @commands.command(name=uncensor_command.name, aliases=uncensor_command.aliases, brief=uncensor_command.brief,
                      description=uncensor_command.description, usage=uncensor_command.usage)
    @commands.has_role('Junta')
    async def unban_word(self, ctx):
        await ctx.send(self.hammer.uncensor_word(ctx.message))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')
