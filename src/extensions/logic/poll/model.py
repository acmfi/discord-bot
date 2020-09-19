import time


class PollModel:
    def __init__(self, user_message, question, flags):
        # Original message with the command which invoke the poll to be created
        self.user_message = user_message

        # Question of the poll
        self.question = question

        # Different answers
        self.options = []

        # Flags used in the command by the invoker
        self.flags = flags

        # String containing the poll which will be sent to the users in the channel
        self.poll_str = ""

        # Object created by the Discord library containing the poll. The value will be set after
        # we send the message with the poll
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
        question = f"**{self.question}**"
        options = "\n".join([str(o) for o in self.options])
        self.poll_str = f"{question}\n\n{options}"

    def get_log(self):
        return f"Log: New poll. Question: {self.question}. Options: {[o.option_str for o in self.options]}"

    def __str__(self):
        return self.poll_str

    def get_reaction_emojis(self):
        # Returns the emojis in a lists
        return [option.emoji.unicode for option in self.options]
