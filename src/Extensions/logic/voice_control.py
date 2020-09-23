from src.Extensions.logic.lib.roles_functions import VOICE_PERMITTED_ROLES_NAMES, have_permitted_rol, \
    str_permitted_roles_names


class VoiceControl:

    def __init__(self):
        self.levantados_ = []

    def levantados_logic(self):
        if len(self.levantados_) == 0:
            result = 'Nadie ha levantado la mano'
        else:
            result = f'Los usuarios que han levantado la mano, en orden de llegada ' \
                     f'siendo el de mas a la izquierda el primero, son:\n {", ".join(self.levantados_)}'
        return result

    def levantar_mano_logic(self, message):
        message_author = message.author
        result = ""

        if message_author.voice is None:
            result = 'No puedes levantar la mano si no estas conectado a un canal de voz'
        elif message_author.mention not in self.levantados_:
            result = "```fix\n" + message_author.display_name + " ha levantado la mano```"
            self.levantados_.append(message_author.mention)

        return result

    def bajar_mano_logic(self, message):
        message_author = message.author
        message_author_mention = message_author.mention

        if message_author.voice is None:
            result = 'No puedes bajar la mano si no estas conectado a un canal de voz'

        elif message_author_mention in self.levantados_:
            result = "```fix\n" + message_author.display_name + " ha bajado la mano```"
            self.levantados_.remove(message_author_mention)
        else:
            result = 'No puedes bajarte la mano si no la has levantado previamente'

        return result

    @staticmethod
    async def silenciar_logic(message):
        message_author = message.author
        message_channel = message.channel
        mentions = message.mentions
        mention_everyone = message.mention_everyone
        result = ''

        if len(mentions) > 0 or mention_everyone:
            if not have_permitted_rol(message_author.roles, VOICE_PERMITTED_ROLES_NAMES):
                result = f'Solo puedes silenciarte a ti mismo si no eres ' \
                         f'{str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
                return result

            if mention_everyone:
                for member in message_channel.members:
                    if member.voice is not None and not have_permitted_rol(member.roles, VOICE_PERMITTED_ROLES_NAMES):
                        await member.edit(mute=True)
                result = "```css\n[Silencio todo el mundo]```"
            else:
                for member in mentions:
                    if have_permitted_rol(member.roles, VOICE_PERMITTED_ROLES_NAMES):
                        result = f'No puedes silenciar a  {member.mention}  ' \
                                 f'ya que es {str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
                    elif member.voice is None:
                        result = f'No puedes silenciar a {member.mention} si no está conectado a un canal de voz'
                    else:
                        await member.edit(mute=True)
                        result = f'A {member.mention} le ha silenciado un ' \
                                 f'{str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
        else:  # No ha mencionado a nadie (autosilenciar)
            if message_author.voice is None:  # Si no estas en ningun canal de voz, VoiceState es None
                result = 'No puedes silenciarte si no estas conectado a un canal de voz'
            else:
                await message_author.edit(mute=True)
                result = f'{message_author.mention} se ha silenciado'

        return result

    @staticmethod
    async def desilenciar_logic(message):
        message_channel = message.channel
        result = ''

        if not have_permitted_rol(message.author.roles, VOICE_PERMITTED_ROLES_NAMES):
            result = f'No puedes desilenciar si no eres {str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)}'
            return result

        if message.mention_everyone:
            for member in message_channel.members:
                if member.voice is not None:
                    await member.edit(mute=False)
            result = "```css\n[A hablar todo el mundo]```"
        else:
            for member in message.mentions:
                if member.voice is None:
                    result = f'No puedes desilenciar a {member.mention} si no está conectado a un canal de voz'
                else:
                    await member.edit(mute=False)
                    result = f'A {member.mention} le ha desilenciado un ' \
                             f'{str_permitted_roles_names(VOICE_PERMITTED_ROLES_NAMES)} :speaking_head:'

        return result
