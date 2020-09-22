from difflib import SequenceMatcher
from src.Extensions.logic.lib.roles_functions import have_permitted_rol, BAN_HAMMER_PERMITTED_ROLES_NAMES


def similar_word(message):
    words = message.split(" ")
    forbidden = [insult for word in words for insult in BanHammer.BLACKLIST if
                 SequenceMatcher(None, insult, word).ratio() > 0.8]
    return forbidden
    # More than 80% similarity


class BanHammer:
    PATH = r'C:\Users\Daniel\OneDrive - Universidad Politécnica de Madrid\Estudios\Python\discord-bot\src\static\blacklist_insultos.txt'
    with open(PATH, 'r') as f:
        BLACKLIST = [line.strip().casefold() for line in f if line.strip().casefold() != ""]

    @staticmethod
    def add_word_blacklist(message):
        word = message.content.split(" ", 1)[1]
        if word in BanHammer.BLACKLIST:
            return "La palabra ya estaba baneada"
        else:
            with open(BanHammer.PATH, 'a') as file:
                file.write("\n" + word)
            BanHammer.BLACKLIST.append(word)
            return 'Palabra censurada correctamente :)'

    @staticmethod
    def get_forbidden_words(message, commands_name):
        # Si comprobamos es comando de /censor o alias(1) y rol de autor es válido (2):
        command_str = message.content.split()[0]
        if have_permitted_rol(message.author.roles, BAN_HAMMER_PERMITTED_ROLES_NAMES) and command_str in commands_name:
            return None
        # Obtenemos lista con palabras invalidas
        return similar_word(message.content)

    @staticmethod
    def uncensor_word(message):
        word = message.content.split(" ", 1)[1]
        if word in BanHammer.BLACKLIST:
            with open(BanHammer.PATH, 'w') as file:
                for line in BanHammer.BLACKLIST:
                    if line.strip("\n") != word and line != "":
                        file.write("\n" + line)
            BanHammer.BLACKLIST.remove(word)
            return 'Palabra descensurada correctamente :)'
        else:
            return "La palabra no está baneada, por lo que no se ha removido"
