from discord.ext import commands
from difflib import SequenceMatcher

PERMITTED_ROLES_NAMES = ('Junta', 'Admin')


def setup(bot):
    bot.add_cog(BanHammerView(bot))


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


class Command:
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

    def get_command_n_aliases(self):
        return [self._prefix + command for command in ([self.name] + self.alias)]


class BanHammerCommand(Command):
    def __init__(self):
        super().__init__("censor", ["censura", "censurar"])
    
    
class BanHammerView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot    
        self.blacklist = BLACKLIST
        Command._prefix = self.bot.command_prefix
        

    @commands.command(name=BanHammerCommand().name, alias=BanHammerCommand().alias)
    @commands.has_role('Junta')
    async def ban_word(self, ctx): 
        await ctx.send(BanHammer().add_word_blacklist(ctx.message))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return None

        forbidden_words_used = BanHammer().get_forbidden_words(message=message, commands_name=BanHammerCommand().get_command_n_aliases())        
        if forbidden_words_used:
            # Delete the message
            await message.delete() 
            # Send an alert through the channel
            await message.channel.send(message.author.mention + ", debes cuidar tu vocabulario, jovencito")            
            # Send a private message to the user
            await message.author.send("El mensaje \n" + str(f'```diff\n-"{message.content}"```') +
                                          "no se ajusta a las normas, en los próximos mensajes no uses: " +
                                          str(forbidden_words_used).strip('[]') + "ni parecidos.")


    @commands.command(name='uncensor')
    @commands.has_role('Junta')
    async def unban_word(self, ctx):      
        await ctx.send(BanHammer().uncensor_word(ctx.message))


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRole):
            await ctx.send('Lo siento, no es nada personal, pero no tienes permiso para hacer eso :)')
