from src.extensions.logic.exceptions.exceptions import InvalidOptionException


"""
Dictionary with the emojis for the numbers. There are two versions. The short one will be used for the 
emojis within the text. But the unicode version will be used for the reaction. These are discord 
requirements.
"""
NUMBER_EMOJIS = {
    "short": [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"],
    "unicode": ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, 10)]
}


class EmojiOption:
    """
    An emoji class will contain useful information about the emojis used for the options.
    It will have two attributes:

    Attributes
        short(string):      The emoji name used in messages within the text
        unicode(string):    The emoji unicode used in the reactions
    """

    def specific(self, short, unicode):
        """
        It will create a specific emoji. Used for YesOrNoPollModel

        Args:
            short(string): The emoji name used in messages
            unicode(string): The emoji unicode used in the reactions

        Returns:
            The object itself
        """
        self.short = short
        self.unicode = unicode
        return self

    def number(self, index):
        """
        It will create an emoji given the number.  Used for MultipleOptionPollModel

        Args:
            index(int): The number which the emoji will have. Between 0 and 9

        Returns:
            EmojiOption: The object itself
        """
        if index < 0 or index > 9:
            raise InvalidOptionException(
                f"Invalid index {index} for emoji. Only valid between 0 and 9")
        self.short = NUMBER_EMOJIS["short"][index]
        self.unicode = NUMBER_EMOJIS["unicode"][index]
        return self

    def __eq__(self, other):
        """
        Compare if `other` contains the same values as `self`

        Args:
            other (EmojiOption): Object which the self object will be compared to.

        Returns:
            boolean: True if both objects contain the same values. False otherwise.
        """
        if isinstance(other, EmojiOption):
            return self.short == other.short and self.unicode == other.unicode
