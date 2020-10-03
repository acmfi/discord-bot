import time
from src.extensions.logic.poll.flags import PollFlagsCommand
from src.extensions.logic.poll.default_values import DEFAULT_DURATION


class PollModel:
    """Basic model for a poll. 

    It will contain all the information for a poll: question, options and flags(configuration)

    Attributes:
        user_message (Message):     A discord class for the messages containing the original message  
        question (string):          Question of the poll
        options (PollOption[]):     The answers for the poll
        flags (PollFlagsCommand[]): Flags used in the command by the invoker
        poll_str (string):          String containing the poll which will be sent to the users in the channel
        bot_message(Message):       Message object created by the Discord library. This Message will be 
                                    the one sent by the bot and containing the poll.
        created_at(number):         Time of creation
        is_active(boolean):         Represents if the poll is active
        duration(number):           The amount of seconds of the poll. -1 means that will long forever
    """

    def __init__(self, user_message, question, flags):
        """
        It will create the poll model. It will be invoked from MultipleOptionPollModel or YesOrNoPollModel. 

        Args:
            user_message (Message):     A discord class for the messages containing the original message  
            question (string):          Question of the poll
            flags (PollFlagsCommand[]): Flags for the poll containing
        """

        self.user_message = user_message
        self.question = question
        self.options = []
        self.flags = flags
        self.poll_str = ""
        self.bot_message = None
        self.created_at = time.time()
        self.is_active = False

        time_flag = list(
            filter(lambda flag: flag.argument == "time", self.flags))
        if len(time_flag) == 0:
            # Check if no-time flag is set
            no_time_flag = list(
                filter(lambda flag: flag.argument == "no-time", self.flags))
            # If no-time flag is set, duration is -1 otherwise we use default value for duration for the poll
            self.duration = PollFlagsCommand.parse_flag_value(None,
                                                              "time", DEFAULT_DURATION) if len(no_time_flag) == 0 else -1
        else:
            self.duration = time_flag[0].value

    def set_poll_str(self):
        """
        It will create the string containing the poll. This string will be used to send to the user.

        Returns:
            string: The poll in string format
        """
        #horizontal_line = "-" * int(len(self.question) * 1)
        #question = f"~~{horizontal_line}~~\n**{self.question}**\n~~{horizontal_line}~~\n"
        question = f"**{self.question}**\n"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}'''time_str_line'''\n\n{options}\n\nResponda"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[o.content for o in self.options]}"

    def __str__(self):
        return self.poll_str

    def get_reaction_emojis(self):
        """
        Creates a list of strings containing the emojis in unicode mode

        Returns:
            string[]: The emojis in unicode mode
        """
        return [option.emoji.unicode for option in self.options]
