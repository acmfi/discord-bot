import sys
from discord.ext import commands

bot = commands.Bot(command_prefix='/')
TOKEN = open('./src/token.txt', 'r').read()


@bot.event
async def on_ready():
    print('Logged in as\n\tName: {0}\n\tId: {1}\n'.format(
        bot.user.name, bot.user.id))


bot.load_extension('src.extensions.views.poll')
bot.run(TOKEN)
