import discord
from discord.ext import commands


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

        forbidden_words_used = [
            i for i in self.blacklist if message.content.casefold().count(i) > 0]

        if(len(forbidden_words_used) > 0):
            await message.delete()  # Delete the message
            # Send a message on the same channel
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")
            await message.author.send("El mensaje \n" + str(""f"```css\n{message.content}```""") + "no se ajusta a las normas, en los próximos mensajes no uses: " + str(forbidden_words_used).strip('[]'))  # Send a private message to the user

    @commands.command(name='censor')
    @commands.has_role('Junta')
    async def ban_word(self, ctx):
        word = ctx.message.content.split(" ", 1)[1]
        if word in self.blacklist:
            await ctx.send("La palabra ya estaba baneada")
        else:
            with open("blacklist_insultos.txt", "a+") as file:
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


def setup(bot):
    bot.add_cog(BanHammer(bot))
