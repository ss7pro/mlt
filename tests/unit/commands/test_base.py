from mock import patch, Mock
import pytest

from mlt.commands.base import Command
from test_utils.io import catch_stdout


def test_command_invalid_action():
    with pytest.raises(NotImplementedError):
        Command({}).action()
