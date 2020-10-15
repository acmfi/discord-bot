from discord.ext import tasks, commands
import asyncio


def setup(bot):
    """function to init this extension file, called in the main

    Args:
        bot (discord.Bot): main bot
    """
    bot.add_cog(ProtectionLink(bot, bot.link_task_queue))


class ProtectionLink(commands.Cog):
    def __init__(self, bot, link_task_queue):
        """init function

        Args:
            bot (discord.Bot): main discord bot
            link_task_queue (tuple of multiprocessing.Queue): the first queue is to receive tasks and the second is to send results
        """
        self.bot = bot
        self.link_task_queue = link_task_queue
        self.send_invitation_link.start()

    def cog_unload(self):
        """close the bot resource
        """
        self.send_invitacion_link.cancel()

    @tasks.loop(seconds=1)
    async def send_invitation_link(self):
        """when it receive some signal from Connection it will prepare the invitation link and send with same way
        """
        frame_available = asyncio.Event()
        asyncio.get_event_loop().add_reader(
            self.bot.link_task_queue[0]._reader.fileno(), frame_available.set)
        await frame_available.wait()
        frame_available.clear()

        self.bot.link_task_queue[0].get()
        # link will be expired in 15 minutes and only one used by user
        link = await self.bot.guilds[0].text_channels[0].create_invite(max_age=900, max_uses=1)
        self.bot.link_task_queue[1].put(str(link))

    @send_invitation_link.before_loop
    async def before_before_resend_post(self):
        """initialize a list of channels before the loop event begin
        """
        await self.bot.wait_until_ready()
