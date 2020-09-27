class InvalidInputException(Exception):
    """
    This exception will be triggered when the values of a command are invalid.
    """
    pass


class InvalidFlagException(Exception):
    """
    This exception will be triggered when the flags of a command are invalid
    """
    pass


class InvalidOptionException(Exception):
    """
    This exception will be triggered when the option of a poll is invalid
    """
    pass
