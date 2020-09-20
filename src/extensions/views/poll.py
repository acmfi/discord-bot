from discord.ext import commands
from src.extensions.logic.poll.manager import PollManager
from src.extensions.logic.poll.command import PollCommand
from src.extensions.logic.exceptions.exceptions import InvalidInputException, InvalidFlagException


def setup(bot):
    bot.add_cog(Poll(bot))


class Poll(commands.Cog):
    def __init__(self, bot_):
        self.bot = bot_
        self.poll_manager = PollManager()

    @commands.command(name='poll', aliases=['encuesta'], brief='Creates a new poll',
                      description=PollCommand().get_description(), usage=PollCommand().get_usage())
    async def create_poll(self, ctx, *args):
        async def send_msg(msg, log):
            await ctx.message.channel.send(msg)
            print(log)

        try:
            poll, is_help = PollCommand().parser(args, ctx.message)
            if is_help:
                await send_msg(f"```{PollCommand().get_usage()}```", f"Log: Help requested {ctx.message.clean_content}")
                return
            print(poll.get_log())
        except InvalidInputException as e:
            await send_msg(f"```{PollCommand().get_usage()}```",
                           f"Log: Invalid input {ctx.message.clean_content} || {e}")
            return
        except InvalidFlagException as e:
            await send_msg(f"```{PollCommand().get_usage()}```",
                           f"Log: Invalid flag {ctx.message.clean_content} || {e}")
            return
        except Exception as e:
            await send_msg(f"```{PollCommand().get_usage()}```",
                           f"Log: Invalid input {ctx.message.clean_content} || {e}")
            return

        await self.poll_manager.add(poll)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.bot.user == user:
            return
        should_be_removed = self.poll_manager.reaction_should_be_removed(
            reaction)
        if should_be_removed:
            await reaction.remove(user)
