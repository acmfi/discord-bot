from discord.ext import tasks, commands
import discord
import base64


def setup(bot):
    """function to init this extension file, called in the main

    Args:
        bot (discord.Bot): main bot
    """
    bot.add_cog(ResendPost(bot, bot.post_queue))


class ResendPost(commands.Cog):
    def __init__(self, bot, post_queue):
        """class init function

        Args:
            bot (discord.Bot): the main discord bot
            post_queue ([type]): queue of the posts used for process tasks, shared resource with api server
        """
        self.bot = bot
        self.aviso_channels = None
        self.resend_post.start()
        self.post_queue = post_queue

    def cog_unload(self):
        """close the bot resource
        """
        self.resend_post.cancel()

    @tasks.loop(seconds=5.0)
    async def resend_post(self):
        """check for post in the queue each 5 seconds, if exists post it will send to discord's channels
        """
        if not self.post_queue.empty():
            post = self.post_queue.get()
            image = None
            if post['photo']:
                image_str = str(post['photo']).encode('ascii')
                image_byte = base64.b64decode(image_str)
                with open('anuncio.png', 'wb+') as image:
                    image.write(image_byte)

            for channel in self.aviso_channels:
                await channel.send(content=(post['caption'] if image else post['text']), file=(discord.File('anuncio.png') if image else None))

    @resend_post.before_loop
    async def before_resend_post(self):
        """initialize a list of channels before the loop event begin
        """
        await self.bot.wait_until_ready()
        self.aviso_channels = [self.bot.get_channel(
            int(channel_id)) for channel_id in self.bot.CONF["channels_id"]]
