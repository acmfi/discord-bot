import discord

client = discord.Client()
TOKEN = open('token.txt', 'r').read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def have_permitted_rol(autor_roles, permitted_roles_):
    for autor_rol in autor_roles:
        if autor_rol in permitted_roles_:
            return True
    return False


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('!Hello'):
        await message.channel.send('Hello!')

    # Cualquier persona puede silenciarse
    elif message.content.startswith('!BajarMano'):
        # Si no estas en ningun canal de voz, VoiceState es None
        if message.author.voice is None:
            await message.channel.send('No puedes bajar la mano si no estas conectado a un canal de voz')
        else:
            try:
                await message.author.edit(mute=True)
                await message.channel.send(message.author.display_name + ' ha bajado la Mano')
            except discord.HTTPException:
                await message.channel.send('Un error ha ocurrido')

    elif message.content.startswith('!LevantarMano'):
        if message.author.voice is None:
            await message.channel.send('No puedes levantar la mano si no estas conectado a un canal de voz')
        else:
            await message.channel.send(
                "```fix\n" + message.author.display_name + " ha levantado la Mano \n```")

    elif message.content.startswith('!Mano'):
        permitted_roles = [rol for rol in message.guild.roles if rol.name == 'Ponente' or rol.name == 'Admin']
        if not have_permitted_rol(message.author.roles, permitted_roles):
            await message.channel.send('No puedes dar la palabra si no eres ponente o admin')
        else:
            # Miramos las menciones hechas (de la manera @usuario)
            for member in message.mentions:
                if member.voice is None:
                    await message.channel.send(
                        'No puedes dar la palabra a alguien que no esté conectado a un canal de voz')
                else:
                    await member.edit(mute=False)
                    await message.channel.send(
                        'A ' + member.display_name + ' le han dado la palabra un admin o ponente')


client.run(TOKEN)
