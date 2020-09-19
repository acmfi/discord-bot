from src.extensions.logic.poll.model import PollModel
from src.extensions.logic.poll.option import PollOption


class YesOrNoPollModel(PollModel):
    def __init__(self, user_message, question, flags=None):
        super().__init__(user_message, question, flags)
        options = ["True", "False"]
        emojis = ["tick", "cross"]
        self.options = [PollOption(o).set_yesno_emoji(e) for o, e in zip(options, emojis)]
        self.set_poll_str()

    def __eq__(self, other):
        if isinstance(other, YesOrNoPollModel):
            return self.question == other.question and self.flags == other.flags \
                and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]
