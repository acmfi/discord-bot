import discord
from discord.ext import commands
from src.util import VOICE_PERMITTED_ROLES_NAMES, have_permitted_rol, str_permitted_roles_names


def setup(bot):
    bot.add_cog(VoiceControl(bot))


class VoiceControl(commands.Cog):

    def __init__(self, bot_):
        self.bot = bot_
        self.levantados_ = []

    @commands.command(name='Levantados', aliases=['levantados'],
                      brief='Muestra los usuarios que han levantado la mano',
                      description='Muestra, en orden de llegada, los usuarios que han levantado la mano')
    async def levantados(self, ctx):
        message = ctx.message
        message_channel = message.channel
        if len(self.levantados_) == 0:
            await message_channel.send('Nadie ha levantado la mano')
        else:
            result = 'Los usuarios que han levantado la mano, en orden de llegada ' \
                     'siendo el de mas a la izquierda el primero, son:\n' + ", ".join(self.levantados_)
            await message_channel.send(result)

    @commands.command(name='LevantarMano', aliases=['levantarmano', 'Levantar', 'levantar'],
                      brief='Levanta la mano(solicita desilencio)',
                      description='Permite levantar la mano para que, posteriormente, un ' +
                                  str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES) + ' te de la palabra')
    async def levantar_mano(self, ctx):
        message = ctx.message
        message_author = message.author
        message_channel = message.channel

        if message_author.voice is None:
            await message_channel.send('No puedes levantar la mano si no estas conectado a un canal de voz')
            return
        if message_author.mention not in self.levantados_:
            await message_channel.send("```fix\n" + message_author.display_name + " ha levantado la mano```")
            self.levantados_.append(message_author.mention)

    @commands.command(name='BajarMano', aliases=['bajarmano', 'Bajar', 'bajar'],
                      brief='Baja la mano(dejas de pedir la palabra)',
                      description='Permite dejar de solicitar hablar si has cambiado de opinion '
                                  'o ya se te ha resuelto la duda')
    async def bajar_mano(self, ctx):
        message = ctx.message
        message_author = message.author
        message_author_mention = message_author.mention
        message_channel = message.channel

        if message_author.voice is None:
            await message_channel.send('No puedes bajar la mano si no estas conectado a un canal de voz')
            return

        if message_author_mention in self.levantados_:
            await message_channel.send("```fix\n" + message_author.display_name + " ha bajado la mano```")
            self.levantados_.remove(message_author_mention)
        else:
            await message_channel.send('No puedes bajarte la mano si no la has levantado previamente')

    @commands.command(name='Silenciar', aliases=['silenciar'], brief='Silenciate a ti mismo o a los demás)',
                      description='Permite sileciarte a ti mismo o si eres ' + str_permitted_roles_names(
                          VOICE_PERMITTED_ROLES_NAMES) + ' silenciar a quienes no lo son',
                      usage='Opcional[@usuario/s|@everyone]')
    async def silenciar(self, ctx):
        message = ctx.message
        message_author = message.author
        message_channel = message.channel
        mentions = message.mentions
        mention_everyone = message.mention_everyone

        if len(mentions) > 0 or mention_everyone:
            if not have_permitted_rol(message_author.roles, VOICE_PERMITTED_ROLES_NAMES):
                await message_channel.send(
                    'Solo puedes silenciarte a ti mismo si no eres ' + str_permitted_roles_names(
                        VOICE_PERMITTED_ROLES_NAMES))
                return
            if mention_everyone:
                for member in message_channel.members:
                    if member.voice is not None and not have_permitted_rol(member.roles, VOICE_PERMITTED_ROLES_NAMES):
                        await member.edit(mute=True)
                await message_channel.send("```css\n[Silencio todo el mundo]```")
            else:
                for member in mentions:
                    if have_permitted_rol(member.roles, VOICE_PERMITTED_ROLES_NAMES):
                        await message_channel.send('No puedes silenciar a ' + member.mention + ' ya que es ' +
                                                   str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES))
                    elif member.voice is None:
                        await message_channel.send(
                            'No puedes silenciar a ' + member.mention + ' si no está conectado a un canal de voz')
                    else:
                        await member.edit(mute=True)
                        await message_channel.send('A ' + member.mention + ' le ha silenciado un ' +
                                                   str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES))
        else:  # No ha mencionado a nadie (autosilenciar)
            if message_author.voice is None:  # Si no estas en ningun canal de voz, VoiceState es None
                await message_channel.send('No puedes silenciarte si no estas conectado a un canal de voz')
            else:
                try:
                    await message_author.edit(mute=True)
                    await message_channel.send(message_author.mention + ' se ha silenciado')
                except discord.HTTPException:
                    await message_channel.send('Un error ha ocurrido')

    @commands.command(name='Desilenciar', aliases=['desilenciar'],
                      brief='Desilencia',
                      description='Permite a un ' + str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES) +
                                  ' desilenciar a uno o varios usuarios',
                      usage='@usuario/s|@everyone')
    async def desilenciar(self, ctx):
        message = ctx.message
        message_channel = message.channel

        if not have_permitted_rol(message.author.roles, VOICE_PERMITTED_ROLES_NAMES):
            await message_channel.send(
                'No puedes desilenciar si no eres ' + str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES))
            return

        if message.mention_everyone:
            for member in message_channel.members:
                if member.voice is not None:
                    await member.edit(mute=False)
            await message_channel.send("```css\n[A hablar todo el mundo]```")
        else:
            for member in message.mentions:
                if member.voice is None:
                    await message_channel.send(
                        'No puedes desilenciar a' + member.mention + 'si no está conectado a un canal de voz')
                else:
                    await member.edit(mute=False)
                    await message_channel.send('A ' + member.mention + ' le ha desilenciado un ' +
                                               str_permitted_roles_names(
                                                   VOICE_PERMITTED_ROLES_NAMES) + ' :speaking_head:')
