from mock import patch
import pytest
import uuid
from subprocess import CalledProcessError

from mlt.utils.process_helpers import run, run_popen, run_popen_unsecure
from test_utils.io import catch_stdout


@patch('mlt.utils.process_helpers.check_output')
def test_run_no_cwd(check_output):
    """Assert a command was called with no current working dir
       This command should return the value of `bar`
    """
    check_output.return_value.decode.return_value = 'bar'
    output = run('ls')
    assert output == 'bar'


@patch('mlt.utils.process_helpers.check_output')
def test_run_cwd(check_output):
    """Assert a command was called with /tmp as working dir
       This command should return the value of `foo`
    """
    check_output.return_value.decode.return_value = 'foo'
    output = run('ls', '/tmp')
    assert output == 'foo'


@patch('mlt.utils.process_helpers.check_output')
def test_run_error(check_output):
    """There was a bad command made, therefore no output"""
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
    """Popen call should succeed"""
    popen.return_value = 0
    result = run_popen(['ls', '/tmp'])
    assert result == 0


@patch('mlt.utils.process_helpers.Popen')
def test_run_popen_unsecure(popen):
    """Popen call should succeed"""
    popen.return_value = 0
    result = run_popen_unsecure('ls /tmp')
    assert result == 0
