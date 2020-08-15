import discord

client = discord.Client()
TOKEN = open('token.txt', 'r').read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$BajarMano'):
        #Cualquier persona puede silenciarse
        await message.author.edit(reason= None, mute=True)
        await message.channel.send('A '+message.author.display_name+' le han bajado la Mano')
        
    if message.content.startswith('$LevantarMano'):
        await message.channel.send(message.author.display_name +' ha levantado la Mano')

    if message.content.startswith('$Mano'):
        #Falta comprobar que al author de este mensaje sea Ponente 
        await Mano(message)
        await message.channel.send('A '+message.author.display_name +' le han levantado la Mano')

#Aux
async def Mano(message: discord.Message):
    user = message.content.split()
    channel_members= message.channel.members
    for member in channel_members:
        if member.display_name == user[1]:
            user= member
            break
    await user.edit(reason= None, mute=False)



client.run(TOKEN)
