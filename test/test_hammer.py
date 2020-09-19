import pytest
from src.extensions.logic.ban_hammer import BanHammer, have_permitted_rol


class SimulatedMessage():
    def __init__(self, msg, author_name, author_role):
        self.content = msg
        self.author = SimulatedAuthor(author_name, author_role)


class SimulatedAuthor():
    def __init__(self, name, role):
        self.name = name
        self.roles = [SimulatedRoles(role)]


class SimulatedRoles():
    def __init__(self, role):
        self.name = role


def load_BLACKLIST():      
    global BLACKLIST  
    with open('src/blacklist_insultos.txt', 'r') as f:
        BLACKLIST = [line.strip().casefold()
                        for line in f if line.strip().casefold() != ""]

                        
load_BLACKLIST() 
Hammer = BanHammer()


def test_insult():    
    assert len(Hammer.get_forbidden_words(SimulatedMessage("Eres un cansaliebres", "Santi", "Normal_User"), commands_name="")) == 1 


def test_no_insult():
    assert len(Hammer.get_forbidden_words(SimulatedMessage("Hola, que tal?", "Santi", "Normal_User"), commands_name="")) == 0


def test_several_insults():    
    assert len(Hammer.get_forbidden_words(SimulatedMessage("Eres muy tonto, imbécil y bacterio", "Santi", "Normal_User"), commands_name="")) == 3




def test_add_new_word():
    Hammer.add_word_blacklist(SimulatedMessage("!censor PalabraABanearTest", "Santi", "Junta"))
    load_BLACKLIST()  
    forbidden_words_used = [i for i in BLACKLIST if "PalabraABanearTest".casefold().count(i) > 0]
    assert len(forbidden_words_used) == 1


def test_add_existing_word():  
    assert Hammer.add_word_blacklist(SimulatedMessage("!censor PalabraABanearTest", "Santi", "Junta")) == "La palabra ya estaba baneada"


def test_remove_existing_word():  
    assert Hammer.uncensor_word(SimulatedMessage("!censor PalabraABanearTest", "Santi", "Junta")) == 'Palabra descensurada correctamente :)'

def test_remove_nonexisting_word():  
    assert Hammer.uncensor_word(SimulatedMessage("!censor PalabraABanearTest2", "Santi", "Junta")) == "La palabra no está baneada, por lo que no se ha removido"


def test_correct_role():  
    assert have_permitted_rol(SimulatedAuthor("User", "Junta").roles)

def test_not_correct_role():  
    assert not have_permitted_rol(SimulatedAuthor("User", "Noob").roles)