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
import pytest
from mock import MagicMock

from mlt.utils.files import fetch_action_arg, is_custom


@pytest.fixture
def open_mock(patch):
    open_mock = MagicMock()
    open_mock.return_value.__enter__.return_value = ['deploy:\n', 'foo']
    return patch('open', open_mock)


@pytest.fixture
def isfile_mock(patch):
    return patch('os.path.isfile')


@pytest.fixture
def json_load_mock(patch):
    return patch('json.load')


def test_fetch_action_arg_file_nonexistent(open_mock):
    fetch_action_arg('build', 'last_build_container')
    open_mock.assert_not_called()


def test_fetch_action_arg_file_present(json_load_mock, isfile_mock, open_mock):
    isfile_mock.return_value = True
    action_data = {'somekey': 'someval'}
    json_load_mock.return_value.get.return_value = action_data

    result = fetch_action_arg('push', 'last_push_container')
    open_mock.assert_called_once()
    json_load_mock.assert_called_once()
    assert result == action_data


def test_fetch_action_arg_is_custom(json_load_mock, isfile_mock, open_mock):
    isfile_mock.return_value = True
    custom = is_custom('deploy:')

    open_mock.assert_called_once()
    isfile_mock.assert_called_once()
    assert custom
