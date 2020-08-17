import discord as disc

client = disc.Client()
TOKEN = open('token.txt', 'r').read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#  Devuelve el usuario (Member),que esta en el canal desde que se ha escrito el mensaje,
#  dado un str con su nombre de usuario de Discord o None si no lo encuentra
def find_user(message: disc.Message):
    message_content = message.content.split()
    channel_members = message.channel.members
    user = None
    for member in channel_members:
        if member.display_name == message_content[1]:
            user = member
            break
    return user


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$Hello'):
        await message.channel.send('Hello!')

    # Cualquier persona puede silenciarse
    elif message.content.startswith('$BajarMano'):
        # Si no estas en ningun canal de voz, VoiceState es None
        if message.author.voice is None:
            await message.channel.send('No puedes silenciarte si no estas conectado a un canal de voz')
        else:
            try:
                await message.author.edit(mute=True)
                await message.channel.send('A ' + message.author.display_name + ' le han bajado la Mano')
            except disc.HTTPException:
                await message.channel.send('Un error ha ocurrido')

    elif message.content.startswith('$LevantarMano'):
        await message.channel.send(message.author.display_name + ' ha levantado la Mano')

    elif message.content.startswith('$Mano'):
        # Falta comprobar que al author de este mensaje sea Ponente
        if message.guild.get_role("ID ROL PONENTE") or message.guild.get_role("ID ROL ADMIN") \
                not in message.author.roles:
            await message.channel.send('No puedes hacer unmute si no eres ponente o admin')
        else:
            await find_user(message).edit(mute=False)
            await message.channel.send('A ' + message.author.display_name + ' le han levantado la Mano')


client.run(TOKEN)
