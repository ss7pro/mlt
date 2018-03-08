from __future__ import print_function

from mock import patch, MagicMock
from mock_open import MockOpen

from mlt.commands.deploy import DeployCommand
from test_utils.io import catch_stdout


@patch('mlt.commands.deploy.files.fetch_action_arg')
@patch('mlt.commands.deploy.config_helpers.load_config')
@patch('mlt.commands.deploy.build_helpers.verify_build')
@patch('mlt.commands.deploy.process_helpers')
@patch('mlt.commands.deploy.kubernetes_helpers')
@patch('mlt.commands.deploy.Template')
@patch('mlt.commands.deploy.open')
@patch('mlt.commands.deploy.Popen')
@patch('mlt.commands.deploy.progress_bar')
@patch('mlt.commands.deploy.os.listdir')
def test_deploy_gce(listdir_mock, progress_bar, popen_mock, open_mock,
                    template, kube_helpers, process_helpers, verify_build,
                    verify_init, fetch_action_arg):
    open_mock = MockOpen()
    listdir_mock.return_value = ['besttacofile', 'besttrumpetfile']
    progress_bar.duration_progress.side_effect = \
        lambda x, y, z: print('Pushing ')
    popen_mock.return_value.poll.return_value = 0

    deploy = DeployCommand({'deploy': True, '--no-push': False})
    deploy.config = {
        'gceProject': 'gcr://tacoprojectbestproject',
        'name': 'besttacoapp',
        'namespace': 'besttaconamespace'
    }
    fetch_action_arg.return_value = 'output'

    with catch_stdout() as caught_output:
        deploy.action()
        output = caught_output.getvalue()

    # assert pushing, deploying, then objs created, then pushed
    pushing = output.find('Pushing ')
    deploying = output.find('Deploying ')
    inspecting = output.find('Inspect created objects by running:\n')
    pushed = output.find('Pushed to ')
    assert all(var >= 0 for var in (deploying, inspecting, pushing, pushed))
    assert deploying < inspecting, pushing < pushed


@patch('mlt.commands.deploy.files.fetch_action_arg')
@patch('mlt.commands.deploy.config_helpers.load_config')
@patch('mlt.commands.deploy.build_helpers.verify_build')
@patch('mlt.commands.deploy.process_helpers')
@patch('mlt.commands.deploy.kubernetes_helpers')
@patch('mlt.commands.deploy.Template')
@patch('mlt.commands.deploy.open')
@patch('mlt.commands.deploy.Popen')
@patch('mlt.commands.deploy.progress_bar')
@patch('mlt.commands.deploy.os.listdir')
def test_deploy_docker(listdir_mock, progress_bar, popen_mock, open_mock,
                       template, kube_helpers, process_helpers, verify_build,
                       verify_init, fetch_action_arg):
    open_mock = MockOpen()
    listdir_mock.return_value = ['besttacofile', 'besttrumpetfile']
    progress_bar.duration_progress.side_effect = \
        lambda x, y, z: print('Pushing ')
    popen_mock.return_value.poll.return_value = 0

    deploy = DeployCommand({'deploy': True, '--no-push': False})
    deploy.config = {
        'registry': 'dockerhub',
        'name': 'besttacoapp',
        'namespace': 'besttaconamespace'
    }
    fetch_action_arg.return_value = 'output'

    with catch_stdout() as caught_output:
        deploy.action()
        output = caught_output.getvalue()

    # assert pushing, deploying, then objs created, then pushed
    pushing = output.find('Pushing ')
    deploying = output.find('Deploying ')
    inspecting = output.find('Inspect created objects by running:\n')
    pushed = output.find('Pushed to ')
    assert all(var >= 0 for var in (deploying, inspecting, pushing, pushed))
    assert deploying < inspecting, pushing < pushed


@patch('mlt.commands.deploy.files.fetch_action_arg')
@patch('mlt.commands.deploy.config_helpers.load_config')
@patch('mlt.commands.deploy.build_helpers.verify_build')
@patch('mlt.commands.deploy.process_helpers')
@patch('mlt.commands.deploy.kubernetes_helpers')
@patch('mlt.commands.deploy.Template')
@patch('mlt.commands.deploy.open')
@patch('mlt.commands.deploy.Popen')
@patch('mlt.commands.deploy.progress_bar')
@patch('mlt.commands.deploy.os.listdir')
def test_deploy_without_push(listdir_mock, progress_bar, popen_mock, open_mock,
                       template, kube_helpers, process_helpers, verify_build,
                       verify_init, fetch_action_arg):
    open_mock = MockOpen()
    listdir_mock.return_value = ['foo', 'bar']
    progress_bar.duration_progress.side_effect = \
        lambda x, y, z: print('Pushing ')
    popen_mock.return_value.poll.return_value = 0

    deploy = DeployCommand({'deploy': True, '--no-push': True})
    deploy.config = {
        'gceProject': 'gcr://projectfoo',
        'name': 'foo',
        'namespace': 'foo'
    }
    fetch_action_arg.return_value = 'output'

    with catch_stdout() as caught_output:
        deploy.action()
        output = caught_output.getvalue()

    # assert pushing, deploying, then objs created, then pushed
    skipping_push = output.find('Skipping image push')
    deploying = output.find('Deploying ')
    inspecting = output.find('Inspect created objects by running:\n')
    assert all(var >= 0 for var in (deploying, inspecting, skipping_push))
    assert skipping_push < deploying < inspecting

    # we should not see pushing/pushed messages
    pushing = output.find('Pushing ')
    pushed = output.find('Pushed to ')
    assert all(var == -1 for var in (pushing, pushed))
