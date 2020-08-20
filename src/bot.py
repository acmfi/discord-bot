import sys
from discord.ext import commands

# It would be nice to use argparse
# https://docs.python.org/3/library/argparse.html
if "--test" in sys.argv:
    from src import test_parser
    test_parser()
    sys.exit(0)

bot = commands.Bot(command_prefix='/')
TOKEN = open('src/token.txt', 'r').read()


@bot.event
async def on_ready():
    print('Logged in as\n\tName: {0}\n\tId: {1}\n'.format(
        bot.user.name, bot.user.id))


bot.load_extension('extensions.poll')
# bot.run(TOKEN)
