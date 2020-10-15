import pytest

from src.extensions.logic.exceptions.exceptions import InvalidFlagException, InvalidInputException, InvalidOptionException
from src.extensions.logic.poll.command import PollCommand
from src.extensions.logic.poll.model.model import PollModel
from src.extensions.logic.poll.model.option import PollOption
from src.extensions.logic.poll.model.flags import PollFlagsCommand
from src.extensions.logic.poll.manager.handler import PollHandler
from src.extensions.logic.poll.model.multiple_option import MultipleOptionPollModel
from src.extensions.logic.poll.model.yesorno import YesOrNoPollModel
from src.extensions.logic.poll.model.emoji import EmojiOption, NUMBER_EMOJIS


class CleanContent:
    def __init__(self, msg):
        self.clean_content = msg


class SimulatedMessage:
    # We are using a Message model given by the Discord API. To simulate that
    # structure we need to convert the msg to a class like this
    def __init__(self, msg):
        self.message = CleanContent(msg)


def get_discord_format_args(question, options, flags):
    return [ff for f in flags for ff in str(f).split(" ")] + [question] + options


def get_expected_poll(question, options, flags):
    if len(options) == 0:
        if question == "":
            return None
        return YesOrNoPollModel(None, question, flags)
    else:
        return MultipleOptionPollModel(None, question, options, flags)


def get_ctx(question, options, flags):
    return SimulatedMessage(f"/poll {' '.join([str(f) for f in flags])} {question} {' '.join(options)}")


def get_variables(question, options, given_flags=[], need_expected_poll=True):
    flags = [PollFlagsCommand(f[1] != '', f[0], "", "", None if f[1] == '' else f[1])
             for f in given_flags]
    discord_format_args = get_discord_format_args(question, options, flags)
    ctx = get_ctx(question, options, flags)
    poll, is_help = PollCommand().parser(discord_format_args, ctx.message)
    if need_expected_poll:
        expected_poll = get_expected_poll(question, options, flags)
        return poll, is_help, expected_poll
    else:
        return poll, is_help


def test_parser1():
    poll, _, expected_poll = get_variables(
        "This is a question", ["Option 1", "Option 2"])
    assert poll == expected_poll


def test_parser2():
    poll, _, expected_poll = get_variables("This is a question", [])
    assert poll == expected_poll


def test_parser3():
    poll, _, expected_poll = get_variables("This is a question",
                                           ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9",
                                            "o10"])
    assert poll == expected_poll


def test_parser4():
    poll, _, expected_poll = get_variables(
        "This is a question", ["o1", "o2"], [("no-time", "")])
    assert poll == expected_poll


def test_parser5():
    poll, _, expected_poll = get_variables(
        "This is a question", ["o1", "o2"], [("no-time", "")])
    assert poll == expected_poll


def test_parser6():
    poll, _, expected_poll = get_variables(
        "This is a question", ["o1", "o2"], [("time", "5m")])
    assert poll == expected_poll


def test_parser7():
    poll, _, expected_poll = get_variables(
        "This is a question", ["o1", "o2"], [("no-time", "")])
    assert poll == expected_poll


def test_parser8():
    poll, _, expected_poll = get_variables(
        "This is a question", [], [("time", "5m")])
    assert poll == expected_poll


def test_parser9():
    poll, _, expected_poll = get_variables(
        "This is a question", [], [("no-time", "")])
    assert poll == expected_poll


def test_help():
    _, is_help = get_variables("", [], [("help", "")], False)
    assert is_help


def test_flags1():
    assert PollFlagsCommand.parse_flag_value(None, "time", "57s") == 57


def test_flags2():
    assert PollFlagsCommand.parse_flag_value(None, "time", "2m") == 2 * 60


def test_flags3():
    assert PollFlagsCommand.parse_flag_value(None, "time", "3h") == 3 * 60 * 60


def test_flags4():
    assert PollFlagsCommand.parse_flag_value(
        None, "time", "1d") == 1 * 24 * 60 * 60


def test_flags5():
    with pytest.raises(InvalidFlagException):
        PollFlagsCommand.parse_flag_value(None, "time", "8ns")


def test_invalid_input1():
    with pytest.raises(InvalidInputException):
        get_variables("This is a question", ["Only one option"], [], False)


def test_invalid_input2():
    with pytest.raises(InvalidInputException):
        get_variables("/poll", [], [], False)


def test_invalid_input3():
    with pytest.raises(InvalidInputException):
        get_variables("This is a question",
                      ["o1", "o2", "o3", "o4", "o5", "o6",
                          "o7", "o8", "o9", "o10", "o11"], [],
                      False)


def test_invalid_input4():
    with pytest.raises(InvalidFlagException):
        get_variables("This is a question", ["o1", "o2"],
                      [("time", "5m"), ("no-time", "")])


def test_invalid_input5():
    with pytest.raises(InvalidFlagException):
        get_variables("This is a question", [
                      "o1", "o2"], [("invalid-flag", "")])


def test_invalid_flag1():
    with pytest.raises(InvalidFlagException):
        PollFlagsCommand(True, "", "", [], None, None)


def test_invalid_flag2():
    flag = PollFlagsCommand(True, "", "", [], None, "default_value")
    assert flag.value_input == "default_value"


def test_create_option1():
    option_content = "This is an option"
    option = PollOption(option_content)
    expected = PollOption(option_content)
    assert option == expected


def test_create_option2():
    option_content = "This is an option"
    option = PollOption(option_content).set_keycap_emoji(3)
    expected = PollOption(option_content)
    expected.emoji = EmojiOption().number(2)
    assert option == expected


def test_create_option3():
    option_content = "This is an option"
    option = PollOption(option_content).set_yesno_emoji("tick")
    expected = PollOption
    expected.option_content = option_content
    expected.emoji = EmojiOption().specific(":white_check_mark:", '\U00002705')
    assert option == expected


def test_create_option4():
    option_content = "This is an option"
    option = PollOption(option_content).set_yesno_emoji("cross")
    expected = PollOption
    expected.option_content = option_content
    expected.emoji = EmojiOption().specific(":x:", '\U0000274c')
    assert option == expected


def test_create_option3():
    option_content = "Invalid index for emoji"
    with pytest.raises(InvalidOptionException):
        PollOption(option_content).set_keycap_emoji(0)
    with pytest.raises(InvalidOptionException):
        PollOption(option_content).set_keycap_emoji(-5)


def test_create_option4():
    option_content = "Invalid index for emoji"
    with pytest.raises(InvalidOptionException):
        PollOption(option_content).set_keycap_emoji(11)
    with pytest.raises(InvalidOptionException):
        PollOption(option_content).set_keycap_emoji(18)


def test_seconds2str1():
    seconds = 55
    assert "55s" == PollHandler.seconds2str(None, seconds)


def test_seconds2str2():
    seconds = 120
    assert "2m" == PollHandler.seconds2str(None, seconds)


def test_seconds2str3():
    seconds = 546
    assert "9m y 6s" == PollHandler.seconds2str(None, seconds)


def test_seconds2str4():
    seconds = 650
    assert "10m y 50s" == PollHandler.seconds2str(None, seconds)


def test_seconds2str5():
    seconds = 35780
    assert "9h y 56m" == PollHandler.seconds2str(None, seconds)


def test_seconds2str6():
    seconds = 43200
    assert "12h" == PollHandler.seconds2str(None, seconds)


def test_seconds2str7():
    seconds = 100001
    assert "1d y 3h" == PollHandler.seconds2str(None, seconds)


def test_seconds2str8():
    seconds = 175000
    assert "2d" == PollHandler.seconds2str(None, seconds)
