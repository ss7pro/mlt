from __future__ import print_function

from mock import patch, MagicMock
from mock_open import MockOpen

from mlt.commands.deploy import Deploy
from test_utils.io import catch_stdout


@patch('mlt.commands.deploy.Deploy._load_config')
@patch('mlt.commands.deploy.Deploy._verify_init')
@patch('mlt.commands.deploy.Deploy._verify_build')
@patch('mlt.commands.deploy.process_helpers')
@patch('mlt.commands.deploy.kubernetes_helpers')
@patch('mlt.commands.deploy.Template')
@patch('mlt.commands.deploy.open')
def test_deploy_gce(load_config_mock, verify_init_mock, verify_build_mock,
                    proc_helpers_mock, kube_helpers_mock, template_mock,
                    open_mock):
    open_mocker = MockOpen()

    deploy = Deploy({'deploy': True})
    deploy.config = {
        'gceProject': 'gcr://tacoprojectbestproject',
        'name': 'besttacoapp',
        'namespace': 'besttaconamespace'
    }
    deploy._fetch_action_arg = lambda x, y: y

    with catch_stdout() as caught_output:
        with patch('mlt.commands.deploy.Popen') as popen_patch:
            with patch('mlt.commands.deploy.progress_bar') as progress_bar:
                with patch('mlt.commands.deploy.os.listdir') as listdir_mock:
                    listdir_mock.return_value = \
                        ['besttacofile', 'besttrumpetfile']
                    progress_bar.duration_progress.side_effect = \
                        lambda x, y, z: print('Pushing ')
                    popen_patch.return_value.poll.return_value = 0

                    deploy.action()

        # assert pushing, deploying, then objs created, then pushed
        output = caught_output.getvalue()

    pushing = output.find('Pushing ')
    deploying = output.find('Deploying ')
    inspecting = output.find('Inspect created objects by running:\n')
    pushed = output.find('Pushed to ')
    assert all(var >= 0 for var in (deploying, inspecting, pushing, pushed))
    assert deploying < inspecting, pushing < pushed


@patch('mlt.commands.deploy.Deploy._load_config')
@patch('mlt.commands.deploy.Deploy._verify_init')
@patch('mlt.commands.deploy.Deploy._verify_build')
@patch('mlt.commands.deploy.process_helpers')
@patch('mlt.commands.deploy.kubernetes_helpers')
@patch('mlt.commands.deploy.Template')
@patch('mlt.commands.deploy.open')
def test_deploy_gce(load_config_mock, verify_init_mock, verify_build_mock,
                    proc_helpers_mock, kube_helpers_mock, template_mock,
                    open_mock):
    open_mocker = MockOpen()

    deploy = Deploy({'deploy': True})
    deploy.config = {
        'registry': 'dockerhub',
        'name': 'besttacoapp',
        'namespace': 'besttaconamespace'
    }
    deploy._fetch_action_arg = lambda x, y: y

    with catch_stdout() as caught_output:
        with patch('mlt.commands.deploy.Popen') as popen_patch:
            with patch('mlt.commands.deploy.progress_bar') as progress_bar:
                with patch('mlt.commands.deploy.os.listdir') as listdir_mock:
                    listdir_mock.return_value = \
                        ['besttacofile', 'besttrumpetfile']
                    progress_bar.duration_progress.side_effect = \
                        lambda x, y, z: print('Pushing ')
                    popen_patch.return_value.poll.return_value = 0

                    deploy.action()

        # assert pushing, deploying, then objs created, then pushed
        output = caught_output.getvalue()

    pushing = output.find('Pushing ')
    deploying = output.find('Deploying ')
    inspecting = output.find('Inspect created objects by running:\n')
    pushed = output.find('Pushed to ')
    assert all(var >= 0 for var in (deploying, inspecting, pushing, pushed))
    assert deploying < inspecting, pushing < pushed
