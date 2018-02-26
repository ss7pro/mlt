from mock import patch
from mlt.commands.undeploy import Undeploy


@patch('mlt.commands.undeploy.Undeploy._load_config')
@patch('mlt.commands.undeploy.Undeploy._verify_init')
@patch('mlt.commands.undeploy.process_helpers')
def test_undeploy(load_config_mock, verify_init_mock, process_helpers_mock):
    undeploy = Undeploy({'undeploy': True})
    process_helpers_mock.assert_called_once()
