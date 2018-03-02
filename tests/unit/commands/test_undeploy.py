from mock import patch
from mlt.commands.undeploy import UndeployCommand


@patch('mlt.commands.undeploy.config_helpers.load_config')
@patch('mlt.commands.undeploy.process_helpers')
def test_undeploy(proc_helpers, load_config):
    undeploy = UndeployCommand({'undeploy': True})
    undeploy.config = {'namespace': 'tacosandtrumpets'}
    undeploy.action()
    proc_helpers.run.assert_called_once()
