from src.extensions.logic.poll.emoji import Emoji


class PollOption:
    def __init__(self, option_str):
        self.option_str = option_str
        self.emoji = None

    def set_keycap_emoji(self, index):
        if index < 1 or index > 11:
            raise Exception(
                f"Invalid emoji index {index}. Only valid between 0 and 9")
        self.emoji = Emoji().number(index - 1)
        return self

    def set_yesno_emoji(self, emoji_type):
        if emoji_type == "tick":
            self.emoji = Emoji().specific(":white_check_mark:", '\U00002705')
        elif emoji_type == "cross":
            self.emoji = Emoji().specific(":x:", '\U0000274c')
        return self

    def __str__(self):
        return f"{self.emoji.short}{' ' * 3}{self.option_str}"

    def __eq__(self, other):
        if isinstance(other, PollOption):
            return self.option_str == other.option_str and self.emoji == other.emoji
