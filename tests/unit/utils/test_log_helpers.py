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

import uuid
from mlt.utils.log_helpers import check_for_pods_readiness

from test_utils.io import catch_stdout


@pytest.fixture
def sleep_mock(patch):
    return patch('sleep')


@pytest.fixture
def process_helpers(patch):
    return patch('process_helpers.run_popen')


def test_check_for_pods_readiness(process_helpers, sleep_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    process_helpers.return_value.stdout.read.return_value = \
        bytearray("\n".join(
            ["random-pod1", "random-pod2",
             filter_tag + "-ps-" + run_id[3] + " 1/1  Running  0  16d",
             filter_tag + "-worker1-" + run_id[3] + " 1/1  Running  0  16d",
             filter_tag + "-worker2-" + run_id[3] + " 1/1  Running  0  16d",
             filter_tag + "-worker2-" + run_id[3] + " 1/1  Completed  0  16d"]
        ), 'utf8')

    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace',
                                         filter_tag=filter_tag, retries=5)
        output = caught_output.getvalue()

    assert found
    assert "Checking for pod(s) readiness" in output


def test_check_for_pods_readiness_no_pods(process_helpers, sleep_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    process_helpers.return_value.stdout.read.return_value = ''

    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace',
                                         filter_tag=filter_tag, retries=1)
        output = caught_output.getvalue()

    assert not found
    assert "Retrying " in output


def test_check_for_pods_readiness_max_retries_reached(process_helpers,
                                                      sleep_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])

    process_helpers.return_value.stdout.read.return_value = \
        bytearray("\n".join(["random-pod1", "random-pod2"]), 'utf8')
    with catch_stdout() as caught_output:
        found = check_for_pods_readiness(namespace='namespace',
                                         filter_tag=filter_tag, retries=5)
        output = caught_output.getvalue()

    assert not found
    assert "Max retries Reached." in output


def test_check_for_pods_readiness_max_retries_when_status_is_not_running(
        process_helpers, sleep_mock):
    run_id = str(uuid.uuid4()).split("-")
    filter_tag = "-".join(["app", run_id[0], run_id[1]])
    process_helpers.return_value.stdout.read.return_value = \
        bytearray("\n".join(
            [filter_tag + "-ps-" + run_id[3] + " 1/1  ContainerCreating  0  "
                                               "16d",
             filter_tag + "-worker1-" + run_id[3] + " 1/1  ContainerCreating  "
                                                    "0  16d",
             filter_tag + "-worker2-" + run_id[3] + " 1/1  ContainerCreating  "
                                                    "0  16d"]
        ), 'utf-8')

    with catch_stdout() as caught_output:
        running = check_for_pods_readiness(namespace='namespace',
                                           filter_tag=filter_tag, retries=4)
        output = caught_output.getvalue()

    assert not running
    assert "Max retries Reached." in output
