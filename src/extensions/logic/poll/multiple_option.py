from src.extensions.logic.poll.model import PollModel
from src.extensions.logic.poll.option import PollOption


class MultipleOptionPollModel(PollModel):
    """Multiple option poll

    A poll with 2 or more options. These options are given by the user and each option will be associated 
    with an emoji with a number (from 0 to 9 in order). This class is inherited from PollModel

    Attributes:
        options (PollOption[]): The answers for the poll
    """

    def __init__(self, user_message, question, options, flags=None):
        """
        It will create the poll model. It will invoke the constructor of PollModel and will initialize 
        the options 

        Args:
            user_message (Message):     A discord class for the messages containing the original message  
            question (string):          Question of the poll
            flags (PollFlagsCommand[]): (Optional) Flags for the poll containing
        """
        super().__init__(user_message, question, flags)
        self.options = [PollOption(o).set_keycap_emoji(i)
                        for i, o in enumerate(options, start=1)]
        self.set_poll_str()

    def __eq__(self, other):
        """
        Compare if `other` contains the same values as `self`

        Args:
            other (MultipleOptionPollModel): Object which the self object will be compared to.

        Returns:
            boolean: True if both objects contain the same values. False otherwise.
        """
        if isinstance(other, MultipleOptionPollModel):
            return self.question == other.question and self.flags == other.flags and self.poll_str == other.poll_str \
                and False not in [o1 == o2 for (o1, o2) in zip(self.options, other.options)]
