from __future__ import print_function

from mock import patch, MagicMock

from mlt.commands.build import BuildCommand
from test_utils.io import catch_stdout


@patch('mlt.commands.build.config_helpers.load_config')
@patch('mlt.commands.build.open')
@patch('mlt.commands.build.process_helpers.run_popen')
@patch('mlt.commands.build.progress_bar')
def test_simple_build(progress_bar, popen, open_mock,
                      verify_init):
    progress_bar.duration_progress.side_effect = \
        lambda x, y, z: print('Building')
    popen.return_value.poll.return_value = 0

    build = BuildCommand({'build': True, '--watch': False})
    build.config = MagicMock()

    with catch_stdout() as caught_output:
        build.action()
        output = caught_output.getvalue()

    # assert that we started build, then did build process, then built
    starting = output.find('Starting build')
    building = output.find('Building')
    built = output.find('Built')
    assert all(var >= 0 for var in (starting, building, built))
    assert starting < building < built


@patch('mlt.commands.build.config_helpers.load_config')
@patch('mlt.commands.build.time.sleep')
@patch('mlt.commands.build.Observer')
@patch('mlt.commands.build.open')
def test_watch_build(open_mock, observer, sleep_mock, verify_init):
    sleep_mock.side_effect = KeyboardInterrupt

    build = BuildCommand({'build': True, '--watch': True})
    build.config = MagicMock()

    with patch('mlt.commands.build.EventHandler') as event_handler_patch:
        build.action()
