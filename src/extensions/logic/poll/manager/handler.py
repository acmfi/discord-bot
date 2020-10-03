import rx
from rx import operators as op
import time
import asyncio
from src.extensions.logic.poll.model.model import PollModel
from src.extensions.logic.poll.default_values import REFRESH_RATE

CLOCKS_EMOJI = [f":clock{hour}:" for hour in range(1, 13)]


class PollHandler:
    """This class will handle the poll

    If the poll has time, then it will refresh every REFRESH_RATE seconds value given in
    default_values.py the message with the poll with the time left for voting. For that purpose,
    the interval will be created using rx. See more details on Reactive Programming for this (variable sub).
    For editing the message, a new thread will be created each time, so do not block
    the main thread (variable _loop)

    Attributes:
        poll(PollModel):    Object with the poll
        sub(Observable):    Observable with the interval. Every REFRESH_RATE seconds will produce a value
        _loop(Observable):  Current event loop. See more details in asyncio. We will use it to create a
                            new thread
    """

    def __init__(self, poll: PollModel):
        """
        Initializes the class. If there is no duration for the poll or is inactive, it only will initialize
        with the poll attribute

        Attributes:
            poll(PollModel):    Object with the poll
        """
        # TODO check if is active
        self.poll = poll

        if self.poll.duration == -1:
            return

        # Use for avoid waiting to edit message
        # https://stackoverflow.com/questions/53722398/how-to-send-a-message-with-discord-py-from-outside-the-event-loop-i-e-from-pyt
        self._loop = asyncio.get_event_loop()

        self.sub = rx.interval(REFRESH_RATE).pipe(
            # Seconds that the poll will last
            op.take_until_with_time(self.poll.duration)
        )

        self.subscribe()

    async def send_poll_n_react(self):
        """
        Sends a message with the poll to the channel which the poll was invoked. Then, for each
        option, the bot will react with the corresponding emoji so users can vote using those 
        reaction. Any other reaction will be removed.
        """
        # Sends the poll
        poll_str = self.__get_msg(-1)
        self.poll.bot_message = await self.poll.user_message.channel.send(poll_str)

        # Reacts to the message with the different emojis associated to the options
        [await self.poll.bot_message.add_reaction(emoji) for emoji in self.poll.get_reaction_emojis()]

    def subscribe(self):
        """
        It subscribes to the Observable. For each iteration will call __on_next or __on_error if something
        went wrong. When finishing it, __on_completed will be executed
        """
        self.sub.subscribe(
            on_next=self.__on_next,
            on_error=self.__on_error,
            on_completed=self.__on_completed
        )

    def __get_msg(self, i):
        """It will create the message to send to the user

        Args:
            i(number): Number of the iteration
        """
        seconds_left = int(self.poll.created_at +
                           self.poll.duration - time.time())
        seconds_left = 5 * round(seconds_left / 5)  # Round seconds to 0 or 5
        time_str = f"*{CLOCKS_EMOJI[i % 12]}  La votación cierra en {self.seconds2str(seconds_left)}*"
        poll_str = str(self.poll).replace(
            "'''time_str_line'''", time_str.rjust(len(time_str) + 5))
        print(poll_str, len(self.poll.question))
        return poll_str

    def __on_next(self, i):
        """It will update the message with the poll with the time left.

        It will calculate the time left rounded to 0 or 5 seconds and then will use seconds2str() to create a more
        readable version of the time. Then it will create the message with the original content of the message. with
        a small animation of a clock moving the clock hands each iteration. For editting the message, the __edit_msg
        function will be used

        Args:
            i(number): Number of the iteration
        """
        # TODO Change is_active lifecycle
        self.poll.is_active = True

        poll_str = self.__get_msg(i)
        self.__edit_msg(poll_str)

    def __on_error(self, iteration):
        pass

    def __on_completed(self):
        """
        It will update the message with the poll: "Poll has ended" and some emojis
        """
        self.poll.is_active = False
        poll_str = f"{str(self.poll)}\n\n:male_dancer::dancer:  La votación ha terminado  :male_dancer::dancer:"
        self.__edit_msg(poll_str)

    def __edit_msg(self, msg):
        """
        It will update the message with the poll. It will create a new thread for that so it does not block main
        thread.

        Args:
            msg(string): String with the new message content
        """
        asyncio.run_coroutine_threadsafe(
            self.poll.bot_message.edit(content=msg), self._loop)

    def seconds2str(self, seconds):
        """
        It will convert the seconds to a string more readable for humans. As an example:
            - 120 -> 2m
            - 650 -> 10m y 50s
            - 35780 -> 9h y 56m

        Args:
            seconds(number): Amount of seconds

        Returns
            string: Human version of the seconds
        """
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
