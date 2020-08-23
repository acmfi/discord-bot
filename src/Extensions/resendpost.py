from discord.ext import tasks, commands
import discord
import base64

def setup(bot):
    bot.add_cog(ResendPost(bot, bot.post_queue, bot.apiserver))

class ResendPost(commands.Cog):
    def __init__(self, bot, post_queue, apiserver):
        self.bot = bot
        self.aviso_channels = None
        self.resend_post.start()
        self.post_queue = post_queue
        self.apiserver = apiserver

    def cog_unload(self):
        self.resend_post.cancel()
        self.apiserver.terminate()

    @tasks.loop(seconds=5.0)
    async def resend_post(self):
        post = self.post_queue.get()
        print(str(post['text']))
        image = None
        if post['photo']:
            print(type(post['photo']))
            image_str= str(post['photo']).encode('ascii')
            image_byte = base64.b64decode(image_str)
            image = open('anuncio.png', 'wb+')
            image.write(image_byte)
            image.close()
        
        for channel in self.aviso_channels:
            print(post['text'])
            await channel.send(content=(post['caption'] if image else post['text']), file=(discord.File('anuncio.png') if image else None))

    @resend_post.before_loop
    async def before_resend_post(self):
        await self.bot.wait_until_ready()
        self.aviso_channels = [self.bot.get_channel(int(channel_id.rstrip('\n'))) for channel_id in open('src/channels_id.txt').readlines()]

