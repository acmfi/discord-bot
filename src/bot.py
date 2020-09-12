from discord.ext import commands
from multiprocessing import Process, Queue
import apiserver
import json

bot = commands.Bot(command_prefix='!')
with open('src/bot_conf.json', 'r') as conf_file:
    bot.CONF = json.load(conf_file) 


@bot.event
async def on_ready():
    print('------------------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')

bot.post_queue = Queue()
apiserver = Process(target=apiserver.run, args=(bot.post_queue,))
apiserver.start()
bot.load_extension('Extensions.resendpost')
bot.run(bot.CONF["token"])
