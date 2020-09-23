from Extensions.logic.lib.roles_functions import str_permitted_roles_names, VOICE_PERMITTED_ROLES_NAMES
from discord.ext import commands

from src.Extensions.logic.lib.command import Command
from src.Extensions.logic.voice_control import VoiceControl


def setup(bot):
    bot.add_cog(VoiceControlView(bot))


class VoiceControlView(commands.Cog):
    levantados_command = Command(name='Levantados', aliases=['levantados'],
                                 brief='Muestra los usuarios que han levantado la mano',
                                 description='Muestra, en orden de llegada, los usuarios que han levantado la mano')

    levantar_mano_command = Command(name='LevantarMano', aliases=['levantarmano', 'Levantar', 'levantar'],
                                    brief='Levanta la mano(solicita desilencio)',
                                    description=f'Permite levantar la mano para que, posteriormente,'
                                                f'un {str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
                                                f'te de la palabra')

    bajar_mano_command = Command(name='BajarMano', aliases=['bajarmano', 'Bajar', 'bajar'],
                                 brief='Baja la mano(dejas de pedir la palabra)',
                                 description='Permite dejar de solicitar hablar si has cambiado de opinion '
                                             'o ya se te ha resuelto la duda')

    silenciar_command = Command(name='Silenciar', aliases=['silenciar'],
                                brief='Silenciate a ti mismo o a los demás)',
                                description=f'Permite sileciarte a ti mismo o si eres '
                                            f'{str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
                                            f'silenciar a quienes no lo son',
                                usage='Opcional[@usuario/s|@everyone]')

    desilenciar_command = Command(name='Desilenciar', aliases=['desilenciar'],
                                  brief='Desilencia',
                                  description=f'Permite a un {str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)} '
                                              f'desilenciar a uno o varios usuarios',
                                  usage='@usuario/s|@everyone')

    def __init__(self, bot_):
        self.bot = bot_
        self.levantados_ = []
        self.voice_control = VoiceControl()

    @commands.command(name=levantados_command.name, aliases=levantados_command.aliases,
                      brief=levantados_command.brief,
                      description=levantados_command.description)
    async def levantados(self, ctx):
        await ctx.message.channel.send(self.voice_control.levantados_logic())

    @commands.command(name=levantar_mano_command.name, aliases=levantar_mano_command.aliases,
                      brief=levantar_mano_command.brief,
                      description=levantar_mano_command.description)
    async def levantar_mano(self, ctx):
        await ctx.message.channel.send(self.voice_control.levantar_mano_logic(ctx.message))

    @commands.command(name=bajar_mano_command.name, aliases=bajar_mano_command.aliases,
                      brief=bajar_mano_command.brief,
                      description=bajar_mano_command.description)
    async def bajar_mano(self, ctx):
        await ctx.message.channel.send(self.voice_control.bajar_mano_logic(ctx.message))

    @commands.command(name=silenciar_command.name, aliases=silenciar_command.aliases,
                      brief=silenciar_command.brief,
                      description=silenciar_command.description,
                      usage=silenciar_command.usage)
    async def silenciar(self, ctx):
        await ctx.message.channel.send(self.voice_control.silenciar_logic(ctx.message))

    @commands.command(name=desilenciar_command.name, aliases=desilenciar_command.aliases,
                      brief=desilenciar_command.brief,
                      description=desilenciar_command.description,
                      usage=desilenciar_command.usage)
    async def desilenciar(self, ctx):
        await ctx.message.channel.send(self.voice_control.desilenciar_logic(ctx.message))
