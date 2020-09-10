import pytest

from src.extensions.poll import InvalidInputException, MultipleOptionPollModel, PollCommand, PollModel, Emoji, EMOJIS, \
    PollOption, \
    YesOrNoPollModel, FlagsPollCommand, seconds2str, InvalidFlagException, parse_flag_value


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
        return YesOrNoPollModel(None, question, flags)
    else:
        return MultipleOptionPollModel(None, question, options, flags)


def get_ctx(question, options, flags):
    return SimulatedMessage(f"/poll {' '.join([str(f) for f in flags])} {question} {' '.join(options)}")


def get_variables(question, options, given_flags=[], need_expected_poll=True):
    flags = [FlagsPollCommand(f[1] != '', f[0], "", "", None if f[1] == '' else f[1])
             for f in given_flags]
    discord_format_args = get_discord_format_args(question, options, flags)
    ctx = get_ctx(question, options, flags)
    if need_expected_poll:
        expected_poll = get_expected_poll(question, options, flags)
        return discord_format_args, ctx, expected_poll
    else:
        return discord_format_args, ctx

def test_parser1():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["Option 1", "Option 2"])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll

    expected_str = "**This is a question**\n\n" \
                   ":zero:   Option 1\n" \
                   ":one:   Option 2"
    assert expected_poll.poll_str == expected_str


def test_parser2():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", [])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser3():
    discord_format_args, ctx, expected_poll = get_variables("This is a question",
                                                            ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9",
                                                             "o10"])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser4():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["o1", "o2"], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser5():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["o1", "o2"], [("invalid-flag", "")])
    with pytest.raises(InvalidFlagException):
        PollCommand().parser(discord_format_args, ctx)


def test_parser6():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["o1", "o2"], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser7():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["o1", "o2"], [("time", "5m")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser8():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", ["o1", "o2"], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll

def test_parser9():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", [], [("time", "5m")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser10():
    discord_format_args, ctx, expected_poll = get_variables("This is a question", [], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_flags1():
    assert parse_flag_value("time", "57s") == 57


def test_flags2():
    assert parse_flag_value("time", "2m") == 2 * 60


def test_flags3():
    assert parse_flag_value("time", "3h") == 3 * 60 * 60


def test_flags4():
    assert parse_flag_value("time", "1d") == 1 * 24 * 60 * 60


def test_invalid_input1():
    discord_format_args, ctx = get_variables("This is a question", ["Only one option"], [], False)
    with pytest.raises(InvalidInputException):
        PollCommand().parser(discord_format_args, ctx)


def test_invalid_input2():
    discord_format_args, ctx = get_variables("/poll", [], [], False)
    with pytest.raises(InvalidInputException):
        PollCommand().parser(discord_format_args, ctx)


def test_invalid_input3():
    discord_format_args, ctx = get_variables("This is a question",
                                             ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10", "o11"], [],
                                             False)
    with pytest.raises(InvalidInputException):
        PollCommand().parser(discord_format_args, ctx)


def test_invalid_input4():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"],
                                                            [("time", "5m"), ("no-time", "")])
    with pytest.raises(InvalidFlagException):
        PollCommand().parser(discord_format_args, ctx)


def test_create_option1():
    option_str = "This is an option"
    option = PollOption(option_str)
    expected = PollOption(option_str)
    assert option == expected


def test_create_option2():
    option_str = "This is an option"
    option = PollOption(option_str).set_keycap_emoji(3)
    expected = PollOption(option_str)
    expected.emoji = Emoji(EMOJIS["short"][2], EMOJIS["unicode"][2])
    assert option == expected


def test_create_option3():
    option_str = "Invalid index for emoji"
    with pytest.raises(Exception):
        PollOption(option_str).set_keycap_emoji(0)
    with pytest.raises(Exception):
        PollOption(option_str).set_keycap_emoji(-5)


def test_create_option4():
    option_str = "Invalid index for emoji"
    with pytest.raises(Exception):
        PollOption(option_str).set_keycap_emoji(11)
    with pytest.raises(Exception):
        PollOption(option_str).set_keycap_emoji(18)


def test_seconds2str1():
    seconds = 55
    assert "55s" == seconds2str(seconds)


def test_seconds2str2():
    seconds = 120
    assert "2m" == seconds2str(seconds)


def test_seconds2str3():
    seconds = 546
    assert "9m y 6s" == seconds2str(seconds)


def test_seconds2str4():
    seconds = 650
    assert "10m y 50s" == seconds2str(seconds)


def test_seconds2str5():
    seconds = 35780
    assert "9h y 56m" == seconds2str(seconds)


def test_seconds2str6():
    seconds = 43200
    assert "12h" == seconds2str(seconds)


def test_seconds2str7():
    seconds = 100001
    assert "1d y 3h" == seconds2str(seconds)


def test_seconds2str8():
    seconds = 175000
    assert "2d" == seconds2str(seconds)
