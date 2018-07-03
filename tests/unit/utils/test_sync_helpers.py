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


# import json
# import os
#
#
# def get_sync_spec():
#     """
#     Returns dict value for 'sync_spec' in case '.sync.json' exists
#     otherwise return None
#     """
#     sync_file = '.sync.json'
#     if os.path.isfile(sync_file):
#         with open(sync_file, 'r') as f:
#             sync_data = json.load(f)
#             if 'sync_spec' in sync_data.keys():
#                 return sync_data['sync_spec']
#
#     return None


import json
import pytest

from mlt.utils.sync_helpers import get_sync_spec


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
def get_sync_spec_mock(patch):
    return patch('get_sync_spec')


def test_get_sync_spec_no_json(isfile_mock, open_mock, json_mock,
                               get_sync_spec_mock):
    """
    Tests if no .sync.json file is present
    """
    isfile_mock.return_value = False
    output = get_sync_spec()
    assert output is None


def test_get_sync_spec_empty_json(isfile_mock, open_mock, json_mock,
                                  get_sync_spec_mock):
    """
    Tests if .sync.json file is empty
    """
    isfile_mock.return_value = True
    json.load.return_value = {}
    output = get_sync_spec()
    assert output is None
