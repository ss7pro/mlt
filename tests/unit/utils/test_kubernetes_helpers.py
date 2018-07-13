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
import pytest
import uuid

from mlt.utils.kubernetes_helpers import (ensure_namespace_exists,
                                          checking_crds_on_k8)


@pytest.fixture
def proc_helpers(patch):
    return patch('process_helpers')


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def call_mock(patch):
    return patch('call')


def test_ensure_namespace_no_exist(proc_helpers, open_mock, call_mock):
    call_mock.return_value = 0

    ensure_namespace_exists(str(uuid.uuid4()))
    proc_helpers.run.assert_not_called()


def test_ensure_namespace_already_exists(proc_helpers, open_mock, call_mock):
    call_mock.return_value = 1

    ensure_namespace_exists(str(uuid.uuid4()))
    proc_helpers.run.assert_called_once()


def test_checking_crds_on_k8(proc_helpers):
    proc_helpers.run_popen.return_value.stdout.read.return_value.decode.\
        return_value = json.dumps({'items': [
                                   {'metadata': {'name': 'tfjob'}}]})
    crd_set = {'tfjob', 'pytorchjob'}
    missing_crds = checking_crds_on_k8(crd_set)
    assert missing_crds == {'pytorchjob'}
