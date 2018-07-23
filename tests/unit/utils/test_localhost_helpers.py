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

from mlt.utils.localhost_helpers import binary_path


@pytest.fixture
def isfile_mock(patch):
    return patch('os.path.isfile')


@pytest.fixture
def ospath_split_mock(patch):
    return patch('os.path.split')


@pytest.fixture
def access_mock(patch):
    return patch('os.access')


def test_binary_path_exists(isfile_mock, access_mock, ospath_split_mock):
    """
    Tests if binary is in path
    """
    isfile_mock.return_value = True
    access_mock.return_value = True
    ospath_split_mock.return_value = ('path', 'name')
    output = binary_path('python')
    assert output == 'python'


def test_binary_path_fpath_exists(isfile_mock, access_mock):
    """
    Tests if binary is in path and fpath is true
    """
    isfile_mock.return_value = True
    access_mock.return_value = True
    output = binary_path('python')
    assert '/bin/python' in output


def test_binary_path_doesnot_exist(isfile_mock, access_mock):
    """
    Tests if binary is not in path
    """
    isfile_mock.return_value = False
    access_mock.return_value = False
    output = binary_path('pyth0n')
    assert output is None


def test_binary_path_not_executable(isfile_mock, access_mock):
    """
    tests if binary is not executable
    """
    isfile_mock.return_value = True
    access_mock.return_value = False
    output = binary_path('test_localhost_helpers.py')
    assert output is None
