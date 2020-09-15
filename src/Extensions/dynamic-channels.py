import discord
from discord.ext import commands

def setup(bot):
    bot.add_cog(DynamicChannels(bot))

class DynamicChannels(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    #This method detects if the voice state update is leaving or joining a voice channel, and if there's
    #a text channel related to that one it changes the permissions for hidding/showing that text channel
    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        #The arguments are: A member-> The one who the Voice state update is related to
        #And two VoiceStates -> The before and after states of the voice update (every action related 
        # to the voice: mute, join/leave channel, etc...)
        both_channels = list(map(lambda x : (str(x)+"-texto").casefold(),[after.channel,before.channel]))
        try:
            if(before.channel == after.channel):  return 0
            for channel in member.guild.channels:
                if channel.type.name == 'text':
                    if str(channel).casefold() == both_channels[1]:
                        await channel.set_permissions(member,read_messages= False, send_messages = False)
                    if str(channel).casefold() == both_channels[0]:
                        await channel.set_permissions(member,read_messages=True, send_messages=True)

        except discord.ext.commands.BotMissingPermissions as de:
            print("Bot is missing permissions to complete this command (Dynamic channels)")