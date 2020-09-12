from difflib import SequenceMatcher

PERMITTED_ROLES_NAMES = ('Junta', 'Admin')

def have_permitted_rol(autor_roles):
    for autor_rol in autor_roles:
        if autor_rol.name in PERMITTED_ROLES_NAMES:
            return True
    return False


def similar_word(message):
    words = message.split(" ")    
    forbidden = [insult for word in words for insult in BLACKLIST if SequenceMatcher(None, insult, word).ratio()>0.8]    
    return forbidden
    # More than 80% similarity


with open('src/blacklist_insultos.txt', 'r') as f:
    BLACKLIST = [line.strip().casefold()
                    for line in f if line.strip().casefold() != ""]
                   

class BanHammer():
    def __init__(self):
        self.blacklist = BLACKLIST

    def add_word_blacklist(self, message):        
        word = message.content.split(" ", 1)[1]        
        if word in self.blacklist:
            return "La palabra ya estaba baneada"
        else:
            with open("src/blacklist_insultos.txt", "a") as file:
                file.write("\n" + word)
            self.blacklist.append(word)
            return 'Palabra censurada correctamente :)'
            
    
    def get_forbidden_words(self, message, commands_name):
        # Si comprobamos es comando de /censor o alias(1) y rol de autor es válido (2):
        command_str = message.content.split()[0]
        if have_permitted_rol(message.author.roles) and command_str in commands_name:        
            return None
        # Obtenemos lista con palabras invalidas
        return similar_word(message.content)


    def uncensor_word(self, message):
        word = message.content.split(" ", 1)[1]        
        if word in self.blacklist:            
            with open("src/blacklist_insultos.txt", "w") as file:
                for line in self.blacklist:
                    if line.strip("\n") != word and line != "":
                        file.write("\n" + line)
            self.blacklist.remove(word)
            return 'Palabra descensurada correctamente :)'
        else:
            return "La palabra no está baneada, por lo que no se ha removido"








    