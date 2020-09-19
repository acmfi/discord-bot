from discord.ext import tasks, commands
import discord
from multiprocessing import Pipe
import asyncio


def setup(bot):
    """fuction to init this extension file, called in the main

    Args:
        bot (discord.Bot): main bot
    """
    bot.add_cog(ProtectionLinkView(bot, bot.link_connection))


class ProtectionLinkView(commands.Cog):
    def __init__(self, bot, link_connection):
        self.bot = bot
        self.link_connection = link_connection
        self.send_invitation_link.start()

    def cog_unload(self):
        self.send_invitacion_link.cancel()

    @tasks.loop(seconds=5.0)
    async def send_invitation_link(self):
        # try:
        #     await self.bot.loop.run_in_executor(None, self.link_connection.recv)
        #     await self.bot.loop.run_in_executor(None, self.link_connection.send, "https://discord.gg/BW2Cjn")
        # except:
        #     print("fallo await")

        frame_available = asyncio.Event()
        asyncio.get_event_loop().add_reader(
            self.bot.link_connection.fileno(), frame_available.set)
        await frame_available.wait()
        frame_available.clear()

        self.bot.link_connection.recv()
        # link will be expired in 15 minutes and only one used by user
        link = await self.bot.guilds[0].text_channels[0].create_invite(max_age=900, max_uses=1)
        self.bot.link_connection.send(str(link))

    @send_invitation_link.before_loop
    async def before_before_resend_post(self):
        """initialize a list of channels before the loop event begin
        """
        await self.bot.wait_until_ready()


class ProtectionLink():
    def __init__(self, bot):
        pass

    def send_invitacion_link(self, pipe):
        pass
