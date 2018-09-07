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
from conditional import conditional

import pytest
from mlt.commands.logs import LogsCommand

from test_utils.io import catch_stdout


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def get_only_one_file(patch):
    def mocker(job_desired, error_msg):
        return job_desired
    return patch('log_helpers.files.get_only_one_job', mocker)


@pytest.fixture
def sleep_mock(patch):
    return patch('log_helpers.sleep')


@pytest.fixture
def process_helpers(patch):
    return patch('log_helpers.process_helpers.run_popen')


@pytest.fixture
def check_for_pods_readiness_mock(patch):
    return patch('log_helpers.check_for_pods_readiness')


@pytest.fixture
def verify_init(patch):
    return patch('config_helpers.load_config')


def call_logs(catch_exception=None, job_name=None):
    logs_command = LogsCommand(
        {'logs': True,
         '--since': '1m',
         '--retries': 5,
         '--job-name': job_name
         })
    logs_command.config = {'name': 'app', 'namespace': 'namespace'}

    with catch_stdout() as caught_output:
        with conditional(catch_exception, pytest.raises(catch_exception)):
            logs_command.action()
        output = caught_output.getvalue().strip()
    return output


def test_logs_get_logs(open_mock, verify_init, sleep_mock,
                       check_for_pods_readiness_mock,
                       get_only_one_file, process_helpers):
    check_for_pods_readiness_mock.return_value = True
    process_helpers.return_value.poll.return_value = 0
    process_helpers.return_value.communicate.return_value = ("log output", '')

    assert call_logs() == "log output"


def test_logs_no_push_json_file(open_mock, verify_init, sleep_mock,
                                process_helpers):
    assert "Please use --job-name flag to pick a job to tail." in call_logs(
        catch_exception=SystemExit)


def test_logs_command_not_found(open_mock, sleep_mock, get_only_one_file,
                                check_for_pods_readiness_mock, verify_init,
                                process_helpers):
    check_for_pods_readiness_mock.return_value = True
    command_not_found = "/bin/sh: kubetail: command not found"
    process_helpers.return_value.poll.return_value = 1
    process_helpers.return_value.communicate.return_value = (None,
                                                             command_not_found)

    assert 'It is a prerequisite' in call_logs(catch_exception=SystemExit)


def test_logs_no_logs_found(open_mock, sleep_mock, get_only_one_file,
                            check_for_pods_readiness_mock, verify_init,
                            process_helpers):
    check_for_pods_readiness_mock.return_value = False

    assert "No logs found for this job." in call_logs()


def test_logs_keyboardinterrupt(open_mock, verify_init, sleep_mock,
                                get_only_one_file,
                                check_for_pods_readiness_mock,
                                process_helpers):
    check_for_pods_readiness_mock.return_value = True
    process_helpers.side_effect = KeyboardInterrupt

    call_logs(catch_exception=SystemExit)
