from discord.ext import commands

PERMITTED_ROLES_NAMES = ('Junta', 'Admin')


def setup(bot):
    bot.add_cog(BanHammer(bot))


def have_permitted_rol(autor_roles):
    for autor_rol in autor_roles:
        if autor_rol.name in PERMITTED_ROLES_NAMES:
            return True
    return False


class BanHammer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('blacklist_insultos.txt', 'r') as f:
            self.blacklist = [line.strip().casefold()
                              for line in f if line.strip().casefold() != ""]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        message_content = message.content
        forbidden_words_used = [
            i for i in self.blacklist if message_content.casefold().count(i) > 0]

        if len(forbidden_words_used) > 0:
            censor_command = self.bot.get_command('censor')
            censor_command_names = censor_command.aliases
            censor_command_names.append(censor_command.name)
            str_ = message_content.split()[0]
            # If one with permitted roles is baning a word, we dont ban his message
            if have_permitted_rol(message.author.roles) and str_[0] == self.bot.command_prefix \
                    and str_[1:] in censor_command_names:
                pass
            else:
                await message.delete()  # Delete the message
                # Send a message on the same channel
                await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")
                # Send a private message to the user
                await message.author.send("El mensaje \n" + str(f'```diff\n-"{message_content}"```') +
                                          "no se ajusta a las normas, en los próximos mensajes no uses: " +
                                          str(forbidden_words_used).strip('[]'))

    @commands.command(name='censor')
    @commands.has_role('Junta')
    async def ban_word(self, ctx):
        word = ctx.message.content.split(" ", 1)[1]
        if word in self.blacklist:
            await ctx.send("La palabra ya estaba baneada")
        else:
            with open("blacklist_insultos.txt", "a") as file:
                file.write("\n" + word)
            self.blacklist.append(word)
            await ctx.send('Palabra censurada correctamente :)')

    @commands.command(name='uncensor')
    @commands.has_role('Junta')
    async def unban_word(self, ctx):
        word = ctx.message.content.split(" ", 1)[1]
        if word in self.blacklist:
            with open("blacklist_insultos.txt", "w") as file:
                for line in self.blacklist:
                    if line.strip("\n") != word and line != "":
                        file.write("\n" + line)
            self.blacklist.remove(word)
            await ctx.send('Palabra descensurada correctamente :)')
        else:
            await ctx.send("La palabra no está baneada, por lo que no se ha removido")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')
