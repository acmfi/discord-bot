import discord
import telebot as tb
import asyncio
import threading
import queue

# index 0 is the discord token and 1 is the telegram bot token
TOKEN = open('token.txt', 'r').readlines()
client = discord.Client()
tele_bot = tb.TeleBot(TOKEN[1].rstrip('\n'))
aviso_channels = None
messages_tele_channel = queue.Queue()

############### Telegram bot event #############
@tele_bot.channel_post_handler(content_types=['text'])
def resend_text_to_discord(post):
    global messages_tele_channel
    messages_tele_channel.put(post.text)
    messages_tele_channel.join()

################ Discord bot event ##############
async def my_background_task():
    await client.wait_until_ready()
    global aviso_channels
    global messages_tele_channel
    #while not client.is_closed:
    while True:
        while not messages_tele_channel.empty():
            for channel in aviso_channels:
                await channel.send(messages_tele_channel.get())
            messages_tele_channel.task_done()
        await asyncio.sleep(10) # task runs every 10 seconds

@client.event
async def on_ready():
    global aviso_channels
    print('We have logged in as {0.user}'.format(client))
    aviso_channels = [client.get_channel(int(channel_id.rstrip('\n'))) for channel_id in open('channels.txt').readlines()]

# tele_bot.polling(none_stop=False, interval=0, timeout=20)
threading.Thread(target=tele_bot.polling, kwargs={'none_stop':False, 'interval':0, 'timeout':20}).start()
client.loop.create_task(my_background_task())
client.run(TOKEN[0].rstrip('\n'))
