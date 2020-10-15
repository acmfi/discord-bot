from src.extensions.logic.poll.model.model import PollModel
from src.extensions.logic.poll.model.option import PollOption


class YesOrNoPollModel(PollModel):
    """Yes or no option poll

    A poll with only the question. Therefore 2 options will be generated automatically. As we are
    computer people, we will use True/False, but this can be Yes/No perfectly. Each option will
    be associated with an emoji a tick (for Yes) and a cross (for No). 
    This class is inherited from PollModel

    Attributes:
        options (PollOption[]): The answers for the poll
    """

    def __init__(self, user_message, question, flags=None):
        """
        It will create the poll model. It will invoke the constructor of PollModel and will initialize 
        the options 

        Args:
            user_message (Message):     A discord class for the messages containing the original message  
            question (string):          Question of the poll
            flags (PollFlagsCommand[]): (Optional) Flags for the poll containing
        """
        super().__init__(user_message, question, flags)
        options = ["True", "False"]
        emojis = ["tick", "cross"]
        self.options = [PollOption(o).set_yesno_emoji(e)
                        for o, e in zip(options, emojis)]
        self.set_poll_str()

    def __eq__(self, other):
        """
        Compare if `other` contains the same values as `self`

        Args:
            other (YesOrNoPollModel): Object which the self object will be compared to.

        Returns:
            boolean: True if both objects contain the same values. False otherwise.
        """
        if isinstance(other, YesOrNoPollModel):
            return self.question == other.question and self.flags == other.flags \
                and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]
