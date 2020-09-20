import time


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
            no_time_flag = list(
                filter(lambda flag: flag.argument == "no-time", self.flags))
            if len(no_time_flag) == 0:
                # TODO
                # self.duration = parse_flag_value("time", DEFAULT_DURATION)
                self.duration = 60
            else:
                self.duration = -1
        else:
            self.duration = time_flag[0].value

    def set_poll_str(self):
        """
        It will create the string containing the poll. This string will be used to send to the user.

        Returns:
            string: The poll in string format
        """

        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[o.option_str for o in self.options]}"

    def __str__(self):
        return self.poll_str

    def get_reaction_emojis(self):
        """
        Creates a list of strings containing the emojis in unicode mode

        Returns:
            string[]: The emojis in unicode mode
        """
        return [option.emoji.unicode for option in self.options]
