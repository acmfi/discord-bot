from discord.ext import commands
from multiprocessing import Process, Queue, Pipe
from apiserver import ApiServer
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
bot.link_task_queue = (Queue(), Queue())
apiserver = ApiServer(bot.post_queue, bot.link_task_queue)
apiserver.start()
bot.load_extension('extensions.resendpost')
bot.load_extension('extensions.protection_link')
bot.run(bot.CONF["token"])
