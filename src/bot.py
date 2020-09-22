from discord.ext import commands


class Bot:

    def __init__(self):
        self.bot = commands.Bot(command_prefix='!')
        with open('token.txt', 'r') as token_file:
            self.TOKEN = token_file.read()

    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

    def run(self):
        self.bot.add_listener(self.on_ready)
        self.bot.load_extension('Extensions.view.voice_control')
        self.bot.run(self.TOKEN)


# Hay que crear un archivo script
bot = Bot()
bot.run()
