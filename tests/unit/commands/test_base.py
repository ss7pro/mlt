from mock import patch, Mock
import pytest

from mlt.commands.base import Command, NeedsBuildCommand, NeedsInitCommand
from test_utils.io import catch_stdout


def test_command_invalid_action():
    with pytest.raises(NotImplementedError):
        Command({}).action()


def test_needs_init_command_bad_init():
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit) as bad_init:
            NeedsInitCommand({})
            assert caught_output.getvalue() == "This command requires you " + \
                "to be in an `mlt init` built directory"
            assert bad_init.value.code == 1


@patch('mlt.commands.build.Build')
def test_needs_build_command_bad_build(BuildClass):
    NeedsBuildCommand({})
    assert BuildClass.return_value.action.called
