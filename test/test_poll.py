import pytest

from src.extensions.poll import MultipleOptionPollModel, PollModel, Emoji, EMOJIS, PollOption, _poll_parser

class SimulatedMessage:
    # We are using a Message model given by the Discord API. To simulate that
    # structure we need to convert the msg to a class like this
    def __init__(self, msg):
        self.clean_content = msg

def test_parser1():
    poll_str = '/poll "This is a question" "Option 1" "Option 2"'
    expected_poll = MultipleOptionPollModel(None, "This is a question", ["Option 1", "Option 2"])
    assert _poll_parser(SimulatedMessage(poll_str)) == expected_poll

def test_parser2():
    poll_str = '/poll Random text "This is a question" Random text "Option 1" Random text "Option 2"'
    expected_poll = MultipleOptionPollModel(None, "This is a question", ["Option 1", "Option 2"])
    assert _poll_parser(SimulatedMessage(poll_str)) == expected_poll

def test_parser3():
    poll_str = '/poll "q" "o1" "o2" "o3" "o4" "o5" "o6" "o7" "o8" "o9" "o10"'
    expected_poll = MultipleOptionPollModel(None, "q", ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"])
    assert _poll_parser(SimulatedMessage(poll_str)) == expected_poll

def test_invalid_input1():
    invalid_command = '/poll "Here your question" "Here an option" "A bad option'
    with pytest.raises(Exception):
        PollModel().from_message(SimulatedMessage(invalid_command))

def test_invalid_input2():
    invalid_command = '/poll "Here your question" "Only one option"'
    with pytest.raises(Exception):
        PollModel().from_message(SimulatedMessage(invalid_command))

def test_invalid_input3():
    invalid_command = '/poll "Just a string"'
    with pytest.raises(Exception):
        PollModel().from_message(SimulatedMessage(invalid_command))

def test_invalid_input4():
    invalid_command = '/poll'
    with pytest.raises(Exception):
        PollModel().from_message(SimulatedMessage(invalid_command))

def test_invalid_input5():
    invalid_command = '/poll'
    with pytest.raises(Exception):
        PollModel().from_message(SimulatedMessage(invalid_command))

def test_invalid_input6():
    invalid_command = '/poll "q" "o1" "o2" "o3" "o4" "o5" "o6" "o7" "o8" "o9" "o10" "o11"'
    with pytest.raises(Exception):
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

def test_create_poll1():
    options = ['Here an option', 'Maybe another option', 'and final option']
    poll_model = MultipleOptionPollModel(None, "Here your question", options)
    expected_str = "**Here your question**\n\n" \
                   ":one:   Here an option\n" \
                   ":two:   Maybe another option\n" \
                   ":three:   and final option"
    expected_poll = MultipleOptionPollModel(None, "Here your question", options)
    expected_poll.poll_str = expected_str
    assert expected_poll == poll_model

def test_create_poll2():
    options = ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"]
    poll_model = MultipleOptionPollModel(None, "q", options)
    expected_str = "**q**\n\n" \
               ":one:   o1\n" \
               ":two:   o2\n" \
               ":three:   o3\n" \
               ":four:   o4\n" \
               ":five:   o5\n" \
               ":six:   o6\n" \
               ":seven:   o7\n" \
               ":eight:   o8\n" \
               ":nine:   o9\n" \
               ":keycap_ten:   o10"
    expected_poll = MultipleOptionPollModel(None, "q", options)
    expected_poll.poll_str = expected_str
    assert expected_poll == poll_model
