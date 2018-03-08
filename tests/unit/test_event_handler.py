from mock import MagicMock, patch

from mlt.event_handler import EventHandler
from test_utils.io import catch_stdout


@patch('mlt.event_handler.call')
def test_dispatch_git(call):
    """if event relates to git we return immediately"""
    event_handler = EventHandler(lambda x: 'foo', {})
    event_handler.dispatch(MagicMock(src_path='./.git'))
    call.assert_not_called()


@patch('mlt.event_handler.call')
def test_dispatch_directory(call):
    """if event is the main dir we do nothing"""
    event_handler = EventHandler(lambda x: 'foo', {})
    event_handler.dispatch(MagicMock(src_path='./'))
    call.assert_not_called()


@patch('mlt.event_handler.open')
@patch('mlt.event_handler.call')
def test_dispatch_is_ignored(call, open_mock):
    """if git check-ignore passes, we do nothing"""
    call.return_value = 0
    event_handler = EventHandler(lambda x: 'foo', {})
    event_handler.dispatch(MagicMock())
    assert event_handler.timer is None


@patch('mlt.event_handler.open')
@patch('mlt.event_handler.call')
def test_dispatch(call, open_mock):
    """normal file event handling"""
    event_handler = EventHandler(lambda x: 'foo', {})
    event_handler.timer = None
    with catch_stdout() as caught_output:
        event_handler.dispatch(MagicMock(src_path='/foo'))
        output = caught_output.getvalue()
    assert output == 'event.src_path /foo\n'
