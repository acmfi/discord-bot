import discord
from discord.ext import commands

PERMITTED_ROLES_NAMES = ('Ponente', 'Admin')


def setup(bot):
    bot.add_cog(VoiceControl(bot))


def have_permitted_rol(autor_roles):
    for autor_rol in autor_roles:
        if autor_rol.name in PERMITTED_ROLES_NAMES:
            return True
    return False


def str_permitted_roles_names():
    return ' o '.join(PERMITTED_ROLES_NAMES)


class VoiceControl(commands.Cog):

    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='BajarMano', aliases=['bajarmano', 'Bajar', 'bajar'], brief='Baja la mano(silencia)',
                      description='Permite sileciarte a ti mismo o si eres ' + str_permitted_roles_names() +
                                  ' silenciar a quienes no lo son',
                      usage='[@usuario/s|@everyone]')
    async def bajar_mano(self, ctx):
        # Los admin y ponente pueden silenciar a quien quieran o a todos (menos a otros ponentes/admins)
        message = ctx.message
        if len(message.mentions) > 0 or message.mention_everyone:
            if not have_permitted_rol(message.author.roles):
                await message.channel.send(
                    'Solo puedes bajarte la mano a ti mismo si no eres ' + str_permitted_roles_names())
                return
            if message.mention_everyone:
                for member in message.channel.members:
                    if member.voice is not None and not have_permitted_rol(member.roles):
                        await member.edit(mute=True)
                await message.channel.send("```css\n[Silencio todo el mundo]```")
            else:
                for member in message.mentions:
                    if have_permitted_rol(member.roles):
                        await message.channel.send('No puedes bajar la mano a ' + member.mention + ' ya que es ' +
                                                   str_permitted_roles_names())
                    elif member.voice is None:
                        await message.channel.send(
                            'No puedes bajar la mano a ' + member.mention + ' si no está conectado a un canal de voz')
                    else:
                        await member.edit(mute=True)
                        await message.channel.send('A ' + member.mention + ' le han bajado la mano un ' +
                                                   str_permitted_roles_names())
        else:  # No ha mencionado a nadie (autosilenciar)
            if message.author.voice is None:  # Si no estas en ningun canal de voz, VoiceState es None
                await message.channel.send('No puedes bajar la mano si no estas conectado a un canal de voz')
            else:
                try:
                    await message.author.edit(mute=True)
                    await message.channel.send(message.author.mention + ' ha bajado la Mano')
                except discord.HTTPException:
                    await message.channel.send('Un error ha ocurrido')

    @commands.command(name='LevantarMano', aliases=['levantarmano', 'Levantar', 'levantar'],
                      brief='Levanta la mano(solicita desilencio)',
                      description='Permite levantar la mano para que, posteriormente, un ' +
                                  str_permitted_roles_names() + ' te de la palabra')
    async def levantar_mano(self, ctx):
        message = ctx.message
        channel = message.channel  # Tiene sentido?
        if message.author.voice is None:
            await channel.send('No puedes levantar la mano si no estas conectado a un canal de voz')
        else:
            await channel.send(
                "```fix\n" + message.author.display_name + " ha levantado la Mano```")

    @commands.command(name='DarMano', aliases=['darmano', 'Dar', 'dar'],
                      brief='Da la mano(desilencia)',
                      description='Permite a un ' + str_permitted_roles_names() +
                                  ' dar la mano o la palabra a uno o varios usuarios',
                      usage='@usuario/s|@everyone')
    async def dar_mano(self, ctx):
        message = ctx.message
        if not have_permitted_rol(message.author.roles):
            await message.channel.send('No puedes dar la palabra si no eres ponente o admin')
        elif message.mention_everyone:
            for member in message.channel.members:
                if member.voice is not None:
                    await member.edit(mute=False)
            await message.channel.send("```css\n[A hablar todo el mundo]```")
        else:
            for member in message.mentions:
                if member.voice is None:
                    await message.channel.send(
                        'No puedes dar la palabra a' + member.mention + 'si no está conectado a un canal de voz')
                else:
                    await member.edit(mute=False)
                    await message.channel.send('A ' + member.mention + ' le han dado la palabra un ' +
                                               str_permitted_roles_names() + ' :speaking_head:')
