import pytest

from src.extensions.poll import PollModel, Poll


def test_parser():
    # Structure that the function has to create
    poll = PollModel("This is a question", ["Option 1", "Option 2"])

    # Convert the object to a string.
    # It contains the following string: '/poll "This is a question" "Option 1" "Option 2"'
    poll_str = "/poll " + str(poll)

    assert Poll(None).poll_parser(poll_str) == poll


def test_invalid_input():
    invalid_command = '/poll "Here your question" "Here an option" "A bad option'
    with pytest.raises(Exception):
        Poll(None).poll_parser(invalid_command)
