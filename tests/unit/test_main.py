import pytest
from mock import MagicMock, patch

from mlt.main import run_command

"""
All these tests assert that given a command arg from docopt we call
the right command
"""


@pytest.mark.parametrize('command',
                         ['build', 'deploy', 'init', 'template', 'templates',
                          'undeploy', 'foo'])
def test_run_command(command):
    # couldn't get this to work as a function decorator
    with patch('mlt.main.COMMAND_MAP', ((command, MagicMock()),)) \
            as COMMAND_MAP:
        run_command({command: True})
        COMMAND_MAP[0][1].return_value.action.assert_called_once()
