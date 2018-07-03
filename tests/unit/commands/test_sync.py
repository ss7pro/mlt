#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

from __future__ import print_function

import pytest

from subprocess import CalledProcessError
from test_utils.io import catch_stdout

from mlt.commands.sync import SyncCommand
from mlt.utils import constants


@pytest.fixture
def init_mock(patch):
    return patch('config_helpers.load_config')


@pytest.fixture
def isfile_mock(patch):
    return patch('os.path.isfile')


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def json_mock(patch):
    return patch('json')


@pytest.fixture
def subprocess_mock(patch):
    return patch('subprocess.check_output')


@pytest.fixture
def default_sync_mock(patch):
    return patch('SyncCommand._default_sync')


@pytest.fixture()
def get_sync_spec_mock(patch):
    return patch('sync_helpers.get_sync_spec')


def sync(create=False, reload=False, delete=False):
    sync_cmd = SyncCommand({"create": create, "reload": reload,
                            "delete": delete})

    with catch_stdout() as caught_output:
        sync_cmd.action()
        output = caught_output.getvalue()
    return output


def test_uninitialized_sync():
    """
    Tests calling the sync command before this app has been initialized.
    """
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            SyncCommand({})
        output = caught_output.getvalue()
        expected_error = "This command requires you to be in an `mlt init` " \
                         "built directory"
        assert expected_error in output


@pytest.mark.parametrize("sync_subcommand", [
    'create',
    'reload',
    'delete',
])
def test_sync_commands_no_enable_sync(sync_subcommand, init_mock, open_mock,
                                      isfile_mock):
    """
    Tests calling the sync create, reload or delete command without
    --enable-sync during initialize.
    """
    isfile_mock.side_effect = [False, False, False]
    sync_subcommand = 'create'
    sync = SyncCommand({sync_subcommand: True})

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            sync.action()
        output = caught_output.getvalue()
        expected_output = "This app is not initialized with " \
                          "'--enable-sync' option"
        assert expected_output in output


def test_sync_synced(init_mock, open_mock, isfile_mock, json_mock,
                     subprocess_mock, get_sync_spec_mock):
    """
    Tests trying to setup sync again
    """
    json_mock.load.side_effect = [{"app_run_id": "123-456-789"},
                                  {"sync_spec": "hello-world"}]
    get_sync_spec_mock.return_value = 'hello-world'

    with pytest.raises(SystemExit):
        output = sync(create=True)
        expected_output = "Syncing has been already setup for this app"
        assert expected_output in output


@pytest.mark.parametrize("sync_subcommand", [
    'create',
    'reload',
    'delete',
])
def test_sync_commands_not_deployed(sync_subcommand, init_mock, open_mock,
                                    isfile_mock):
    """
    Tests calling the sync create, reload or delete command before the app has
    been deployed.
    """
    isfile_mock.side_effect = [True, False, False]
    sync_subcommand = 'create'
    sync = SyncCommand({sync_subcommand: True})

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            sync.action()
        output = caught_output.getvalue()
        expected_output = "This app has not been deployed yet"
        assert expected_output in output


def test_successful_sync(init_mock, open_mock, isfile_mock, json_mock,
                         get_sync_spec_mock, subprocess_mock):
    """
    Tests successful call to the sync create command.
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.return_value = {"app_run_id": "123-456-789"}
    get_sync_spec_mock.return_value = None
    expected_output = "Syncing spec is created successfully"
    subprocess_mock.return_value.decode.return_value = expected_output
    sync_output = sync(create=True)
    assert expected_output in sync_output


@pytest.mark.parametrize("sync_command", [
    'sync(reload=True)',
    'sync(delete=True)',
])
def test_reload_delete_not_synced(sync_command, init_mock, open_mock,
                                  isfile_mock, json_mock, subprocess_mock,
                                  get_sync_spec_mock):
    """
    Tests reloading sync agent or deleting sync spec before sync setup
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.return_value = {"app_run_id": "123-456-789"}
    get_sync_spec_mock.return_value = None

    with pytest.raises(SystemExit):
        output = eval(sync_command)
        expected_output = "No syncing spec has been created for this app yet"
        assert expected_output in output


def test_reload_synced(init_mock, open_mock, isfile_mock, json_mock,
                       subprocess_mock, get_sync_spec_mock):
    """
    Tests reloading sync agent after sync create
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.return_value = {"app_run_id": "123-456-789"}
    get_sync_spec_mock.return_value = "hello-world"
    expected_output = "Sync agent is restarted"
    subprocess_mock.return_value.decode.return_value = expected_output
    sync_output = sync(reload=True)
    assert expected_output in sync_output


def test_delete_synced(init_mock, open_mock, isfile_mock, json_mock,
                       get_sync_spec_mock, subprocess_mock):
    """
    Tests delete sync spec after sync setup
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.side_effect = [{"app_run_id": "123-456-789"},
                                  {"sync_spec": "hello-world"}]
    get_sync_spec_mock.return_value = "hello-world"
    expected_output = "Syncing spec is successfully deleted"
    subprocess_mock.return_value.decode.return_value = expected_output
    sync_output = sync(delete=True)
    assert expected_output in sync_output


def test_sync_create_not_in_makefile(init_mock, open_mock, isfile_mock,
                                     get_sync_spec_mock, json_mock,
                                     subprocess_mock):
    """
    Tests use case where sync create target is not in the Makefile.
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.side_effect = [{"app_run_id": "123-456-789"},
                                  {"sync_spec": "hello-world"}]
    get_sync_spec_mock.return_value = None
    error_msg = "This app does not support the `mlt sync create` command"
    subprocess_mock.side_effect = CalledProcessError(
        returncode=2, cmd="make sync-create", output=error_msg)
    sync_output = sync(create=True)
    assert error_msg in sync_output


def test_sync_reload_not_in_makefile(init_mock, open_mock, isfile_mock,
                                     get_sync_spec_mock, json_mock,
                                     subprocess_mock):
    """
    Tests use case where sync reload target is not in the Makefile.
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.side_effect = [{"app_run_id": "123-456-789"},
                                  {"sync_spec": "hello-world"}]
    get_sync_spec_mock.return_value = 'hello-world'
    error_msg = "This app does not support the `mlt sync reload` command"
    subprocess_mock.side_effect = CalledProcessError(
        returncode=2, cmd="make sync-reload", output=error_msg)
    sync_output = sync(reload=True)
    assert error_msg in sync_output


def test_sync_delete_not_in_makefile(init_mock, open_mock, isfile_mock,
                                     get_sync_spec_mock, json_mock,
                                     subprocess_mock):
    """
    Tests use case where sync delete target is not in the Makefile.
    """
    isfile_mock.side_effect = [True, True, False]
    mlt_config = {
        "namespace": "foo",
        "registry": "bar",
        "name": "hello-world",
        constants.TEMPLATE_PARAMETERS: {
            "num_workers": 2
        }
    }
    init_mock.return_value = mlt_config
    json_mock.load.side_effect = [{"app_run_id": "123-456-789"},
                                  {"sync_spec": "hello-world"}]
    get_sync_spec_mock.return_value = 'hello-world'
    error_msg = "This app does not support the `mlt sync delete` command"
    subprocess_mock.side_effect = CalledProcessError(
        returncode=2, cmd="make sync-delete", output=error_msg)
    sync_output = sync(delete=True)
    assert error_msg in sync_output
