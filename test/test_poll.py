import pytest

from src.extensions.poll import PollModel, Poll


def test_parser1():
    # Structure that the function has to create
    expected_poll = PollModel("This is a question", ["Option 1", "Option 2"])

    # Convert the object to a string.
    # It contains the following string: '/poll "This is a question" "Option 1" "Option 2"'
    poll_str = str(expected_poll)

    assert Poll(None).poll_parser(poll_str) == expected_poll

def test_parser2():
    # Structure that the function has to create
    expected_poll = PollModel("This is a question", ["Option 1", "Option 2"])

    poll_str = '/poll Random text "This is a question" Random text "Option 1" Random text "Option 2"'

    assert Poll(None).poll_parser(poll_str) == expected_poll

def test_invalid_input1():
    invalid_command = '/poll "Here your question" "Here an option" "A bad option'
    with pytest.raises(Exception):
        Poll(None).poll_parser(invalid_command)

def test_invalid_input2():
    invalid_command = '/poll "Here your question" "Only one option"'
    with pytest.raises(Exception):
        Poll(None).poll_parser(invalid_command)

def test_invalid_input3():
    invalid_command = '/poll "Just a string"'
    with pytest.raises(Exception):
        Poll(None).poll_parser(invalid_command)

def test_invalid_input4():
    invalid_command = '/poll'
    with pytest.raises(Exception):
        Poll(None).poll_parser(invalid_command)
