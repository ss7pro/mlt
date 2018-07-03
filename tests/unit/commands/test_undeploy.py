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

from mock import patch

from mlt.commands.undeploy import UndeployCommand
import pytest
from test_utils.io import catch_stdout


@pytest.fixture
def json_mock(patch):
    return patch('json')


@pytest.fixture
def os_path_mock(patch):
    return patch('os.path')


@pytest.fixture
def init_mock(patch):
    return patch('config_helpers.load_config')


@pytest.fixture
def is_custom_mock(patch):
    return patch('files.is_custom')


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def subprocess_mock(patch):
    return patch('subprocess.check_output')


@pytest.fixture
def get_sync_spec_mock(patch):
    return patch('sync_helpers.get_sync_spec')


def test_undeploy_custom_undeploy(json_mock, open_mock, init_mock,
                                  get_sync_spec_mock, subprocess_mock,
                                  is_custom_mock, os_path_mock):
    """
    Tests successful call to the undeploy command
    """
    undeploy = UndeployCommand({'undeploy': True})
    undeploy.config = {'name': 'bar', 'namespace': 'foo', 'template': 'test'}
    json_mock.load.return_value = {"app_run_id": "123-456-789"}
    get_sync_spec_mock.return_value = None
    is_custom_mock.return_value = True
    os_path_mock.return_value = True
    undeploy.action()


@patch('mlt.commands.undeploy.config_helpers.load_config')
@patch('mlt.commands.undeploy.process_helpers')
def test_undeploy(proc_helpers, load_config):
    undeploy = UndeployCommand({'undeploy': True})
    undeploy.config = {'namespace': 'foo', 'template': 'test'}
    undeploy.action()
    proc_helpers.run.assert_called_once()


@patch('mlt.commands.undeploy.config_helpers.load_config')
@patch('mlt.commands.undeploy.process_helpers')
def test_undeploy_synced(proc_helpers, load_config, get_sync_spec_mock):
    undeploy = UndeployCommand({'undeploy': True})
    undeploy.config = {'namespace': 'foo', 'template': 'test'}
    get_sync_spec_mock.return_value = 'hello-world'
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            undeploy.action()
        output = caught_output.getvalue()
    expected_output = "This app is currently being synced, please run "\
                      "`mlt sync delete` to unsync first"
    assert expected_output in output
