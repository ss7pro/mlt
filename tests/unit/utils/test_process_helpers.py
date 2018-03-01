from mock import patch
import pytest
import uuid
from subprocess import CalledProcessError

from mlt.utils.process_helpers import run, run_popen
from test_utils.io import catch_stdout


@patch('mlt.utils.process_helpers.check_output')
def test_run_no_cwd(check_output):
    check_output.return_value.decode.return_value = 'tacos and salad'
    output = run('ls')
    assert output == 'tacos and salad'


@patch('mlt.utils.process_helpers.check_output')
def test_run_cwd(check_output):
    check_output.return_value.decode.return_value = 'trumpetseverywhere'
    output = run('ls', '/tmp')
    assert output == 'trumpetseverywhere'


@patch('mlt.utils.process_helpers.check_output')
def test_run_error(check_output):
    check_output.side_effect = CalledProcessError(
        returncode=2, cmd='Bad Command!')
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            run('ls')
        output = caught_output.getvalue().strip()
    # since we're mocking CalledProcessError call, not sure we can simulate
    # exception raised by actual check_output call, so e.output is None
    assert output == 'None'


@patch('mlt.utils.process_helpers.Popen')
def test_run_popen(popen):
    popen.return_value = 0
    result = run_popen(['ls', '/tmp'])
    assert result == 0
