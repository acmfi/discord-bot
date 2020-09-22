import discord
from discord.ext import commands
from src.Extensions.logic.lib.roles_functions import VOICE_PERMITTED_ROLES_NAMES, have_permitted_rol, str_permitted_roles_names

class VoiceControl:

    def __init__(self):
        self.levantados_ = []

    def levantados_logic(self):
        if len(self.levantados_) == 0:
            result='Nadie ha levantado la mano'
        else:
            result = f'Los usuarios que han levantado la mano, en orden de llegada siendo el de mas a la izquierda el primero, son:\n {", ".join(self.levantados_)}'
        return result
