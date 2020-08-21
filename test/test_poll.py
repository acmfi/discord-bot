import pytest

from src.extensions.poll import PollModel, Poll

class SimulatedMessage:
    # We are using a Message model given by the Discord API. To simulate that
    # structure we need to convert the msg to a class like this
    def __init__(self, msg):
        self.clean_content = msg

def test_parser1():
    # Structure that the function has to create
    expected_poll = PollModel("This is a question", ["Option 1", "Option 2"])

    # Convert the object to a string.
    # It contains the following string: '/poll "This is a question" "Option 1" "Option 2"'
    poll_str = str(expected_poll)

    assert PollModel().from_message(SimulatedMessage(poll_str)) == expected_poll

def test_parser2():
    # Structure that the function has to create
    expected_poll = PollModel("This is a question", ["Option 1", "Option 2"])

    poll_str = '/poll Random text "This is a question" Random text "Option 1" Random text "Option 2"'

    assert PollModel().from_message(SimulatedMessage(poll_str)) == expected_poll

def test_parser3():
    # Structure that the function has to create
    expected_poll = PollModel("q", ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"])

    poll_str = '/poll "q" "o1" "o2" "o3" "o4" "o5" "o6" "o7" "o8" "o9" "o10"'

    assert PollModel().from_message(SimulatedMessage(poll_str)) == expected_poll

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

def test_create_poll_test1():
    poll_model = PollModel("Here your question", ['Here an option', 'Maybe another option', 'and final option'])
    expected = "**Here your question**\n\n" \
               ":one:   Here an option\n" \
               ":two:   Maybe another option\n" \
               ":three:   and final option"
    poll_str = str(poll_model)
    poll_model_generated = PollModel().from_message(SimulatedMessage(poll_str))
    assert poll_model_generated.poll_str == expected and \
           poll_model_generated.reactions["short"] == [":one:", ":two:", ":three:"]

def test_create_poll_test2():
    poll_model = PollModel("q", ["o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10"])
    expected = "**q**\n\n" \
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
    poll_str = str(poll_model)
    poll_model_generated = PollModel().from_message(SimulatedMessage(poll_str))
    assert poll_model_generated.poll_str == expected and \
           poll_model_generated.reactions["short"] == [":one:", ":two:", ":three:", ":four:", ":five:", ":six:",
                                                       ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
