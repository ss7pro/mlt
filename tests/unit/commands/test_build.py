from __future__ import print_function

from mock import patch, MagicMock
from mock_open import MockOpen

from mlt.commands.build import Build
from test_utils.io import catch_stdout


@patch('mlt.commands.build.Build._load_config')
@patch('mlt.commands.build.Build._verify_init')
@patch('mlt.commands.build.open')
def test_simple_build(load_config_mock, verify_init_mock, open_mocker):
    open_mocker = MockOpen()
    build = Build({'build': True, '--watch': False})
    build.config = MagicMock()
    with catch_stdout() as caught_output:
        with patch('mlt.commands.build.run_popen') as popen_patch:
            with patch('mlt.commands.build.progress_bar') as progress_bar:
                progress_bar.duration_progress.side_effect = \
                    lambda x, y, z: print('Building')
                popen_patch.return_value.poll.return_value = 0
                build.action()

        # assert that we started build, then did build process, then built
        output = caught_output.getvalue()
        build_start = output.find('Starting build')
        building_start = output.find('Building')
        built_start = output.find('Built')
        assert build_start < building_start < built_start


@patch('mlt.commands.build.Build._load_config')
@patch('mlt.commands.build.Build._verify_init')
@patch('mlt.commands.build.time.sleep')
@patch('mlt.commands.build.Observer')
@patch('mlt.commands.build.open')
def test_watch_build(load_config_mock, verify_init_mock, sleep_mock,
                     observer_mock, open_mocker):
    open_mocker = MockOpen()
    sleep_mock.side_effect = KeyboardInterrupt
    build = Build({'build': True, '--watch': True})
    build.config = MagicMock()
    with patch('mlt.commands.build.EventHandler') as event_handler_patch:
        build.action()
