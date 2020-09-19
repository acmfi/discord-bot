from src.extensions.logic.poll.model import PollModel
from src.extensions.logic.poll.option import PollOption


class MultipleOptionPollModel(PollModel):
    def __init__(self, user_message, question, options, flags=None):
        super().__init__(user_message, question, flags)
        self.options = [PollOption(o).set_keycap_emoji(i) for i, o in enumerate(options, start=1)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question and self.flags == other.flags and self.poll_str == other.poll_str \
                and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]
