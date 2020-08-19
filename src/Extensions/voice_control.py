import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(VoiceControl(bot))


def have_permitted_rol(autor_roles, permitted_roles_):
    for autor_rol in autor_roles:
        if autor_rol in permitted_roles_:
            return True
    return False


class VoiceControl(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_

    @commands.command(name='BajarMano', aliases=['bajarmano', 'Bajar', 'bajar'], brief='Baja la mano(silencia)',
                      description='Permite sileciarte a ti mismo o si eres Admin o Ponente silenciar a quienes no lo son',
                      usage='""|@usuario/s|@everyone', help='ayuda¿?')
    async def bajar_mano(self, ctx):
        # Los admin y ponente pueden silenciar a quien quieran o a todos (menos a otros ponentes/admins)
        message = ctx.message
        if len(message.mentions) > 0 or message.mention_everyone:
            permitted_roles = [rol for rol in ctx.guild.roles if rol.name == 'new role' or rol.name == 'Admin']
            if not have_permitted_rol(message.author.roles, permitted_roles):
                await message.channel.send('Solo puedes bajarte la mano a ti mismo si no eres Admin o Ponente')
                return
            if message.mention_everyone:
                for member in message.channel.members:
                    if member.voice is not None and not have_permitted_rol(member.roles, permitted_roles):
                        await member.edit(mute=True)
                await message.channel.send("```css\n[Silencio todo el mundo]```")
            else:
                for member in message.mentions:
                    if have_permitted_rol(member.roles, permitted_roles):
                        await message.channel.send(
                            'No puedes bajar la mano a ' + member.mention + ' ya que es Admin o Ponente')
                    elif member.voice is None:
                        await message.channel.send(
                            'No puedes bajar la mano a ' + member.mention + ' si no está conectado a un canal de voz')
                    else:
                        await member.edit(mute=True)
                        await message.channel.send(
                            'A ' + member.mention + ' le han bajado la mano un admin o ponente')
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
                      description='Permite levantar la mano para que, posteriormente, un Admin o Ponente te de la palabra',
                      usage='""', help='ayuda¿?')
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
                      description='Permite a un Admin o Ponente dar la mano o la palabra a uno o varios usuarios',
                      usage='@usuario/s', help='ayuda¿?')
    async def dar_mano(self, ctx):
        message = ctx.message
        permitted_roles = [rol for rol in message.guild.roles if rol.name == 'new role' or rol.name == 'Admin']
        if not have_permitted_rol(message.author.roles, permitted_roles):
            await message.channel.send('No puedes dar la palabra si no eres ponente o admin')
        else:
            # # Miramos las menciones hechas (de la manera @usuario)
            # if len(message.mentions) == 0:
            #     await message.channel.send('Escribe a quien quieres dar la palabra de esta manera "!Mano @usuario"')
            for member in message.mentions:
                if member.voice is None:
                    await message.channel.send(
                        'No puedes dar la palabra a' + member.mention + 'si no está conectado a un canal de voz')
                else:
                    await member.edit(mute=False)
                    await message.channel.send(
                        'A ' + member.mention + ' le han dado la palabra un admin o ponente :speaking_head:')
