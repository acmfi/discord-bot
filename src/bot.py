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
    if message.author == client.user or not message.content.startswith('!'):
        return

    elif message.content.startswith('!Hello'):
        await message.channel.send('Hello! :raised_hand:')

    # Cualquier persona puede silenciarse
    # Los admin y ponente pueden silenciar a quien quieran o a todos (menos ellos mismos)
    elif message.content.startswith('!BajarMano'):
        if len(message.mentions) > 0 or message.mention_everyone:
            permitted_roles = [rol for rol in message.guild.roles if rol.name == 'new role' or rol.name == 'Admin']
            if not have_permitted_rol(message.author.roles, permitted_roles):
                await message.channel.send('Solo puedes bajarte la mano a ti mismo si no eres Admin o Ponente')
            else:
                if message.mention_everyone:
                    for member in message.channel.members:
                        if member.voice is not None and not have_permitted_rol(member.roles, permitted_roles):
                            await member.edit(mute=True)
                    await message.channel.send("```css\n[Silencio todo el mundo]```")
                else:
                    for member in message.mentions:
                        if member.voice is None:
                            await message.channel.send(
                                'No puedes bajar la mano a ' + member.mention + ' si no está conectado a un canal de voz')
                        else:
                            await member.edit(mute=True)
                            await message.channel.send(
                                'A ' + member.mention + ' le han bajado la mano un admin o ponente')
        else:
            # Si no estas en ningun canal de voz, VoiceState es None
            if message.author.voice is None:
                await message.channel.send('No puedes bajar la mano si no estas conectado a un canal de voz')
            else:
                try:
                    await message.author.edit(mute=True)
                    await message.channel.send(message.author.mention + ' ha bajado la Mano')
                except discord.HTTPException:
                    await message.channel.send('Un error ha ocurrido')

    elif message.content.startswith('!LevantarMano'):
        if message.author.voice is None:
            await message.channel.send('No puedes levantar la mano si no estas conectado a un canal de voz')
        else:
            await message.channel.send(
                "```fix\n" + message.author.display_name + " ha levantado la Mano```")

    elif message.content.startswith('!Mano'):
        permitted_roles = [rol for rol in message.guild.roles if rol.name == 'new role' or rol.name == 'Admin']
        if not have_permitted_rol(message.author.roles, permitted_roles):
            await message.channel.send('No puedes dar la palabra si no eres ponente o admin')
        else:
            # Miramos las menciones hechas (de la manera @usuario)
            if len(message.mentions) == 0:
                await message.channel.send('Escribe a quien quieres dar la palabra de esta manera "!Mano @usuario"')
            for member in message.mentions:
                if member.voice is None:
                    await message.channel.send(
                        'No puedes dar la palabra a alguien que no esté conectado a un canal de voz')
                else:
                    await member.edit(mute=False)
                    await message.channel.send(
                        'A ' + member.mention + ' le han dado la palabra un admin o ponente :speaking_head:')


client.run(TOKEN)
