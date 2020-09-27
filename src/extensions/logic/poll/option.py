from src.extensions.logic.poll.emoji import Emoji


class PollOption:
    """
    An option of the poll

    Attributes
        option_str(string): The content of the option
        emoji(Emoji):       Emoji object associated to the option
    """

    def __init__(self, option_str):
        """
        It will create the option object without the emojis. Emojis will be initialized using 
        set_keycap_emoji(for numbers) or set_yesno_emoji(for tick/cross)

        Args:
            option_str(string): The content of the option
        """
        self.option_str = option_str
        self.emoji = None

    def set_keycap_emoji(self, index):
        """
        It will initialize the emojis with numbers for MultiplePollOption

        Args:
            index(number):  Must be between 1 and 10. This is the number which 
                            the emoji will have

        Returns:
            PollOption: The object itself
        """
        self.emoji = Emoji().number(index - 1)
        return self

    def set_yesno_emoji(self, emoji_type):
        """
        It will initialize the emojis with a tick or cross for YesOrNoPollModel

        Args:
            emoji_type(string): "tick" | "cross" - Yes or no respectively

        Returns:
            PollOption: The object itself
        """
        # TODO Raise expcetion if emoji_type != tick or cross
        if emoji_type == "tick":
            self.emoji = Emoji().specific(":white_check_mark:", '\U00002705')
        elif emoji_type == "cross":
            self.emoji = Emoji().specific(":x:", '\U0000274c')
        return self

    def __str__(self):
        """
        It will create a string with the emoji and the content. It will be used
        in the message with the poll which will be send to the user.

        Returns:
            string: Option in string format
        """
        return f"{self.emoji.short}{' ' * 3}{self.option_str}"

    def __eq__(self, other):
        """
        Compare if `other` contains the same values as `self`

        Args:
            other (PollOption): Object which the self object will be compared to.

        Returns:
            boolean: True if both objects contain the same values. False otherwise.
        """
        if isinstance(other, PollOption):
            return self.option_str == other.option_str and self.emoji == other.emoji
