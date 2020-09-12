from discord.ext import commands
from discord import user


from funcionalidades.ban_hammer import BanHammer
from funcionalidades.command import Command
from funcionalidades.ban_hammer_command import BanHammerCommand

def setup(bot):
    bot.add_cog(BanHammerView(bot))


class BanHammerView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        Command._prefix = self.bot.command_prefix
        

    @commands.command(name=BanHammerCommand().name, alias=BanHammerCommand().alias)
    @commands.has_role('Junta')
    async def ban_word(self, ctx): 
        await ctx.send(BanHammer().add_word_blacklist(ctx.message))


    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return None
            

        if(type(message.author) is user.User):#Está interactuando con el bot, no en el canal general  
            return None


        forbidden_words_used = BanHammer().get_forbidden_words(message=message, commands_name=BanHammerCommand().get_command_n_aliases())        
        if forbidden_words_used:
            # Delete the message
            await message.delete() 
            # Send an alert through the channel
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")            
            # Send a private message to the user        
            await message.author.send("El mensaje {} no se ajusta a las normas, intenta no usar {} ni parecidos"
            .format(str(f'```diff\n- "{message.content}"```'),str(forbidden_words_used).strip('[]')))


    @commands.command(name='uncensor')
    @commands.has_role('Junta')
    async def unban_word(self, ctx):      
        await ctx.send(BanHammer().uncensor_word(ctx.message))


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')