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
bot.link_connection, connection = Pipe(duplex=True)
apiserver = ApiServer(bot.post_queue, connection)
apiserver.start()
bot.load_extension('extensions.resendpost')
bot.load_extension('extensions.protection_link')
bot.run(bot.CONF["token"])
