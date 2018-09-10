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
import uuid
from mlt.commands.events import EventsCommand
from test_utils.io import catch_stdout


@pytest.fixture
def open_mock(patch):
    return patch('open')


@pytest.fixture
def get_only_one_job(patch):
    def mocker(job_desired, error_msg):
        return job_desired
    return patch('files.get_only_one_job', mocker)


@pytest.fixture
def process_helpers(patch):
    return patch('process_helpers.run_popen')


@pytest.fixture
def verify_init(patch):
    return patch('config_helpers.load_config')


def get_events(catch_exception=None, job_name=None):
    events_command = EventsCommand({'events': True, '--job-name': job_name})
    events_command.config = {'name': 'app', 'namespace': 'namespace'}

    with catch_stdout() as caught_output:
        with conditional(catch_exception, pytest.raises(catch_exception)):
            events_command.action()
        output = caught_output.getvalue().strip()
    return output

# END SIMILAR STUFF TO TEST_LOGS


def test_events_get_events(open_mock, verify_init, process_helpers,
                           get_only_one_job):
    head_value = bytearray("LAST SEEN   FIRST SEEN   COUNT", 'utf-8')
    # technically event_value is different from app_run_id
    # but didn't want to set a global app_run_id
    # if others disagree, I'm not super opposed to it
    job = 'app-{}'.format(uuid.uuid4())
    event_value = bytearray(job, 'utf-8')
    process_helpers.return_value.stdout.readline.side_effect = \
        [head_value, event_value, bytearray('', 'utf-8')]
    process_helpers.return_value.poll.return_value = 1
    process_helpers.return_value.stderr.readline.return_value = ''

    events = get_events(job_name=job)
    assert head_value.decode('utf-8') in events
    assert event_value.decode('utf-8') in events


def test_events_no_push_json_file(open_mock, verify_init, process_helpers):
    error_msg = "Please use --job-name flag to query for job events."
    assert error_msg in get_events(catch_exception=SystemExit)


def test_events_no_resources_found(open_mock, verify_init,
                                   get_only_one_job, process_helpers):
    process_helpers.side_effect = Exception("No resources found")

    assert "No resources found" in get_events(catch_exception=SystemExit)


def test_events_no_events_to_display(open_mock, verify_init,
                                     get_only_one_job, process_helpers):
    head_value = "LAST SEEN   FIRST SEEN   COUNT"
    process_helpers.return_value.stdout.readline.side_effect = \
        [head_value, bytearray("current job events missing", 'utf-8'),
         bytearray('', 'utf-8')]
    process_helpers.return_value.poll.return_value = 1
    process_helpers.return_value.stderr.readline.return_value = ''

    assert "No events to display for this job" in get_events()
