from discord.ext import commands
from multiprocessing import Process, Queue
import apiserver

bot = commands.Bot(command_prefix='!')
TOKEN = open('src/token.txt', 'r').read()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.post_queue = Queue()
bot.apiserver = Process(target=apiserver.run, args=(bot.post_queue,))
bot.apiserver.start()
bot.load_extension('Extensions.resendpost')
bot.run(TOKEN)