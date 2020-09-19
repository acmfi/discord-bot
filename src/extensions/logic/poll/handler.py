import rx
from rx import operators as op
import time
import asyncio
from src.extensions.logic.poll.model import PollModel
from src.extensions.logic.poll.default_values import REFRESH_RATE

CLOCKS_EMOJI = [f":clock{hour}:" for hour in range(1, 13)]


class PollHandler:
    def __init__(self, ctx, poll: PollModel):
        self.poll = poll

        if self.poll.duration == -1:
            return

        self.ob = rx.interval(REFRESH_RATE)
        self.sub = self.ob.pipe(
            # Seconds that the poll will last
            op.take_until_with_time(self.poll.duration)
        )

        # Use for avoid waiting to edit message
        # https://stackoverflow.com/questions/53722398/how-to-send-a-message-with-discord-py-from-outside-the-event-loop-i-e-from-pyt
        self._loop = asyncio.get_event_loop()

        self.subscribe()

    async def send_poll_n_react(self, ctx):
        # Send the poll
        self.poll.bot_message = await ctx.message.channel.send(str(self.poll))

        # React to the message with the different emojis associated to the options
        [await self.poll.bot_message.add_reaction(emoji) for emoji in self.poll.get_reaction_emojis()]

    def subscribe(self):
        self.sub.subscribe(
            on_next=self.__on_next,
            on_error=lambda e: self.__on_error(e),
            on_completed=self.__on_completed
        )

    def __on_next(self, i):
        self.poll.is_active = True
        seconds_left = int(self.poll.created_at +
                           self.poll.duration - time.time())
        seconds_left = 5 * round(seconds_left / 5)  # Round seconds to 0 or 5
        poll_str = f"{str(self.poll)}\n\n{CLOCKS_EMOJI[i % 12]}  La votación cierra en {self.seconds2str(seconds_left)}"
        self.__edit_msg(poll_str)

    def __on_error(self, iteration):
        pass

    def __on_completed(self):
        self.poll.is_active = False
        poll_str = f"{str(self.poll)}\n\n:male_dancer::dancer:  La votación ha terminado  :male_dancer::dancer:"
        self.__edit_msg(poll_str)

    def __edit_msg(self, msg):
        asyncio.run_coroutine_threadsafe(
            self.poll.bot_message.edit(content=msg), self._loop)

    def seconds2str(self, seconds):
        n_days = int(seconds / (24 * 60 * 60))
        if n_days > 0:
            n_hours = int((seconds % (24 * 60 * 60)) / (60 * 60))
            if n_hours > 0:
                return f"{n_days}d y {n_hours}h"
            else:
                return f"{n_days}d"
        n_hours = int(seconds / (60 * 60))
        if n_hours > 0:
            n_minutes = int((seconds % (60 * 60)) / 60)
            if n_minutes > 0:
                return f"{n_hours}h y {n_minutes}m"
            else:
                return f"{n_hours}h"
        n_minutes = int(seconds / 60)
        if n_minutes > 0:
            n_seconds = seconds % 60
            if n_seconds > 0:
                return f"{n_minutes}m y {n_seconds}s"
            else:
                return f"{n_minutes}m"
        return f"{seconds}s"
