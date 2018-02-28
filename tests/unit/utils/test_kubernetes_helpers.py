from mock import patch
from mock_open import MockOpen
import uuid

from mlt.utils.kubernetes_helpers import ensure_namespace_exists


@patch('mlt.utils.kubernetes_helpers.call')
@patch('mlt.utils.kubernetes_helpers.open')
@patch('mlt.commands.init.process_helpers')
def test_ensure_namespace_no_exist(call_mock, open_mocker, proc_helpers_mock):
    call_mock.return_value = 0
    ensure_namespace_exists(str(uuid.uuid4()))
    assert proc_helpers_mock.assert_not_called()


@patch('mlt.utils.kubernetes_helpers.call')
@patch('mlt.utils.kubernetes_helpers.open')
@patch('mlt.commands.init.process_helpers')
def test_ensure_namespace_already_exists(call_mock, open_mocker,
                                         proc_helpers_mock):
    new_namespace = str(uuid.uuid4())
    ensure_namespace_exists(new_namespace)
    ensure_namespace_exists(new_namespace)
    assert proc_helpers_mock.assert_called_once()
