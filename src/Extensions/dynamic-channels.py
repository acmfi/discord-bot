import discord
from discord.ext import commands
def setup(bot):
    bot.add_cog(DynamicChannels(bot))

class DynamicChannels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        #Si se trata de una acción dentro del mismo canal significa que no ha entrado ni salido de un canal
        both_channels = list(map(lambda x : (str(x)+"-texto").casefold(),[after.channel,before.channel]))
        try:
            if(before.channel == after.channel):  return 0
            for channel in member.guild.channels:
                if channel.type.name == 'text':
                    if str(channel).casefold() == both_channels[1]:
                        await channel.set_permissions(member,read_messages= False, send_messages = False)
                    if str(channel).casefold() == both_channels[0]:
                        await channel.set_permissions(member,read_messages=True, send_messages=True)

        except discord.DiscordException as de:
            pass