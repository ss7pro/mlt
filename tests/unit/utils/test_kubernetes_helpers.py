from mock import patch
from mock_open import MockOpen
import uuid

from mlt.utils.kubernetes_helpers import ensure_namespace_exists


@patch('mlt.utils.kubernetes_helpers.call')
@patch('mlt.utils.kubernetes_helpers.open')
@patch('mlt.utils.kubernetes_helpers.process_helpers')
def test_ensure_namespace_no_exist(proc_helpers, open_mock, call):
    call.return_value = 0
    open_mock = MockOpen()

    ensure_namespace_exists(str(uuid.uuid4()))
    proc_helpers.run.assert_not_called()


@patch('mlt.utils.kubernetes_helpers.call')
@patch('mlt.utils.kubernetes_helpers.open')
@patch('mlt.utils.kubernetes_helpers.process_helpers')
def test_ensure_namespace_already_exists(proc_helpers, open_mock, call):
    open_mock = MockOpen()
    call.return_value = 1

    ensure_namespace_exists(str(uuid.uuid4()))
    proc_helpers.run.assert_called_once()
