import pytest

from src.extensions.poll import InvalidInputException, MultipleOptionPollModel, PollCommand, PollModel, Emoji, EMOJIS, \
    PollOption, \
    YesOrNoPollModel, FlagsPollCommand, seconds2str, InvalidFlagException


class CleanContent:
    def __init__(self, msg):
        self.clean_content = msg


class SimulatedMessage:
    # We are using a Message model given by the Discord API. To simulate that
    # structure we need to convert the msg to a class like this
    def __init__(self, msg):
        self.message = CleanContent(msg)


def get_variables(question, options, given_flags=[]):
    flags = [FlagsPollCommand(f[1] != '', f[0], "", "", None if f[1] == '' else f[1])
             for f in given_flags]
    discord_format_args = [str(f) for f in flags] + [question] + options
    if len(options) == 0:
        expected_poll = YesOrNoPollModel(None, question, flags)
    else:
        expected_poll = MultipleOptionPollModel(None, question, options, flags)
    ctx = SimulatedMessage(f"/poll {' '.join([str(f) for f in flags])} {question} {' '.join(options)}")
    return discord_format_args, expected_poll, ctx


def test_parser1():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["Option 1", "Option 2"])
    print(ctx.message.clean_content)
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser2():
    discord_format_args, expected_poll, ctx = get_variables("This is a question",
                                                            ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9",
                                                             "o10"])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser3():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser4():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"], [("invalid-flag", "")])
    with pytest.raises(InvalidFlagException):
        PollCommand().parser(discord_format_args, ctx)


def test_parser5():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"], [("no-time", "")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser6():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"], [("time", "5m")])
    assert PollCommand().parser(discord_format_args, ctx) == expected_poll


def test_parser7():
    discord_format_args, expected_poll, ctx = get_variables("This is a question", ["o1", "o2"],
                                                            [("no-time", "NO_VALUE")])
    with pytest.raises(Exception):
        PollCommand().parser(discord_format_args, ctx)


def test_flags1():
    expected = FlagsPollCommand(True, "time", "", [], "57s")
    assert expected.parse_value() == 57


def test_flags2():
    expected = FlagsPollCommand(True, "time", "", [], "2m")
    expected.parse_value()
    assert expected.parse_value() == 2 * 60


def test_flags3():
    expected = FlagsPollCommand(True, "time", "", [], "3h")
    expected.parse_value()
    assert expected.parse_value() == 3 * 60 * 60


def test_flags4():
    expected = FlagsPollCommand(True, "time", "", [], "1d")
    expected.parse_value()
    assert expected.parse_value() == 1 * 24 * 60 * 60


def test_invalid_input1():
    invalid_command = '/poll "Here your question" "Only one option"'
    with pytest.raises(InvalidInputException):
        PollModel().from_message(SimulatedMessage(invalid_command))


def test_invalid_input2():
    invalid_command = '/poll'
    with pytest.raises(InvalidInputException):
        PollModel().from_message(SimulatedMessage(invalid_command))


def test_invalid_input3():
    invalid_command = '/poll'
    with pytest.raises(InvalidInputException):
        PollModel().from_message(SimulatedMessage(invalid_command))


def test_invalid_input4():
    invalid_command = '/poll "q" "o1" "o2" "o3" "o4" "o5" "o6" "o7" "o8" "o9" "o10" "o11"'
    with pytest.raises(InvalidInputException):
        PollModel().from_message(SimulatedMessage(invalid_command))


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


def test_create_multiple_poll1():
    options = ['Here an option', 'Maybe another option', 'and final option']
    poll_model = MultipleOptionPollModel(None, "Here your question", options, None)
    expected_str = "**Here your question**\n\n" \
                   ":one:   Here an option\n" \
                   ":two:   Maybe another option\n" \
                   ":three:   and final option"
    expected_poll = MultipleOptionPollModel(None, "Here your question", options, None)
    expected_poll.poll_str = expected_str
    assert expected_poll == poll_model


def test_create_multiple_poll2():
    options = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"]
    poll_model = MultipleOptionPollModel(None, "q", options, None)
    expected_str = "**q**\n\n" \
                   ":zero:   o1\n" \
                   ":one:   o1\n" \
                   ":two:   o2\n" \
                   ":three:   o3\n" \
                   ":four:   o4\n" \
                   ":five:   o5\n" \
                   ":six:   o6\n" \
                   ":seven:   o7\n" \
                   ":eight:   o8\n" \
                   ":nine:   o9"
    expected_poll = MultipleOptionPollModel(None, "q", options, None)
    expected_poll.poll_str = expected_str
    assert expected_poll == poll_model


def test_create_yesorno_poll1():
    poll_model = YesOrNoPollModel(None, "Is JS the best language?", None)
    expected_str = "**Is JS the best language?**\n\n" \
                   ":white_check_mark:   True\n" \
                   ":x:   False"
    expected_poll = YesOrNoPollModel(None, "Is JS the best language?", None)
    expected_poll.poll_str = expected_str
    assert expected_poll == poll_model


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
