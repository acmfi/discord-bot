from difflib import SequenceMatcher
from src.Extensions.logic.lib.roles_functions import have_permitted_rol, BAN_HAMMER_PERMITTED_ROLES_NAMES


def similar_word(message):
     """
    check if the message has forbidden words (or a similar word)
        Args:
            message: the message object which contains the phrase to check

        Returns:
            String list: a list with the words that matches with a forbidden word
        """
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
        
         """
        Add a word to the blacklist file
            Args:
             message: the message object which contains the phrase or word to add

        Returns:
            String: A string which describes whether the operation was successful
        """
        
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

        """
        Get the text from the message, check if it is a normal message (and then call similar_word() 
        to check for forbidden words) or if the uncensor command is being used (and the user 
        has the correct role) so the message should not be removed.
            Args:
             message: the message object which contains the phrase or word to check 
             commands_name: The command that has been used (if it has been used)

        Returns:
            String list: A list with the words that matches with a forbidden word
        """

        # Si comprobamos es comando de /censor o alias(1) y rol de autor es válido (2):
        command_str = message.content.split()[0]
        if have_permitted_rol(message.author.roles, BAN_HAMMER_PERMITTED_ROLES_NAMES) and command_str in commands_name:
            return None
        # Obtenemos lista con palabras invalidas
        return similar_word(message.content)

    @staticmethod
    def uncensor_word(message):

         """
        Get the text from the message, check if the word is in the blacklist and if it is then remove it.
            Args:
             message: the message object which contains the phrase or word to remove 
             
        Returns:
            String: A string which describes whether the operation was successful
        """

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
