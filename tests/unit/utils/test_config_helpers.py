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
import json
# io lib supports both python2 and python3 but there's issues with resolving
# test_update_config test when using io lib for python2 so going with cString
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from mock import MagicMock
import pytest

from mlt.utils import constants
from mlt.utils.config_helpers import (load_config,
                                      get_template_parameters as
                                      get_template_params,
                                      get_template_parameters_from_file,
                                      update_config)
from test_utils.io import catch_stdout


@pytest.fixture
def json_mock(patch):
    return patch('json')


@pytest.fixture
def open_mock(patch):
    open_mock = MagicMock()
    open_mock.return_value.__enter__.return_value = 'description'
    return patch('open', open_mock)


@pytest.fixture
def isfile_mock(patch):
    return patch('os.path.isfile', MagicMock(return_value=True))


@pytest.fixture
def get_template_parameters_mock(patch):
    return patch('get_template_parameters')


def test_load_config(json_mock, open_mock, isfile_mock):
    json_mock.load.return_value = {'foo': 'bar'}
    assert load_config() == {'foo': 'bar'}


def test_update_config(open_mock):
    # need to create it empty because in python2 it is read-only if defined
    # # https://docs.python.org/2/library/stringio.html#cStringIO.StringIO
    const_dict = StringIO()
    const_dict.write('{"foo": "bar"}')
    open_mock.return_value.__enter__.return_value = const_dict
    json_data = {'new': 'vals'}
    update_config(json_data)
    assert json.loads(const_dict.getvalue()) == {'new': 'vals'}


def test_needs_init_command_bad_init():
    with catch_stdout() as output:
        with pytest.raises(SystemExit) as bad_init:
            load_config()
            assert output.getvalue() == "This command requires you to" \
                " be in an `mlt init` built directory"
            assert bad_init.value.code == 1


def test_get_empty_template_params():
    config = {"namespace": "foo", "registry": "bar",
              constants.TEMPLATE_PARAMETERS: {}}
    assert get_template_params(config) == {}


def test_get_template_params():
    config = {"namespace": "foo", "registry": "bar",
              constants.TEMPLATE_PARAMETERS:
                  {"epochs": "10", "num_workers": "4"}}
    assert get_template_params(config) == \
        {"epochs": "10", "num_workers": "4"}


def test_get_template_params_from_file(get_template_parameters_mock,
                                       open_mock, isfile_mock, json_mock):
    get_template_parameters_mock.return_value = {'param': 'value'}
    assert get_template_parameters_from_file('file_path') == \
        {'param': 'value'}
