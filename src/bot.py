import discord

client = discord.Client()
TOKEN = open('token.txt', 'r').read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_voice_state_update(member,before,after):
    #Si se trata de una acción dentro del mismo canal significa que no ha entrado ni salido de un canal
    if(before.channel == after.channel):  return 0
    for channel in member.guild.channels:
        if str(channel).casefold() in list(map(lambda x : (str(x)+"-texto").casefold(),[after.channel,before.channel])) and channel.type.name=='text':
            if(before.channel == None):
                await channel.set_permissions(member,read_messages=True,send_messages= True)
            else:
                await channel.set_permissions(member,read_messages= False, send_messages = False)
            break
        


client.run(TOKEN)
