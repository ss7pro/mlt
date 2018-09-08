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

from mlt.utils.files import (fetch_action_arg, is_custom, get_job_kinds,
                             get_only_one_job)

from test_utils.io import catch_stdout

# to support python2
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError


@pytest.fixture
def open_mock(patch):
    open_mock = MagicMock()
    open_mock.return_value.__enter__.return_value = ['deploy:\n', 'foo']
    return patch('open', open_mock)


@pytest.fixture
def isfile_mock(patch):
    return patch('os.path.isfile')


@pytest.fixture
def listdir_mock(patch):
    return patch('os.listdir', MagicMock(return_value=['file1', 'file2']))


@pytest.fixture
def json_load_mock(patch):
    return patch('json.load')


@pytest.fixture
def yaml_load_mock(patch):
    return patch('yaml.load_all', lambda x: [{'kind': 'the-best-kind'}])


@pytest.fixture
def get_deployed_jobs_mock(patch):
    return patch('get_deployed_jobs')


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


def test_get_only_one_job_no_job_desired(get_deployed_jobs_mock):
    """this is old behavior, return the only job in the list"""
    get_deployed_jobs_mock.return_value = ['k8s/job-asdf-1234']
    job = get_only_one_job(None, '')
    assert job == 'k8s/job-asdf'


def test_get_only_one_job_job_desired(get_deployed_jobs_mock):
    """If we have multiple jobs returned and only want 1, return that one"""
    get_deployed_jobs_mock.return_value = ['k8s/job-asdf-1234',
                                           'k8s/job-jkl;-1234']
    job = get_only_one_job('k8s/job-asdf-1234', '')
    assert job == 'k8s/job-asdf'


def test_get_only_one_job_many_jobs(get_deployed_jobs_mock):
    """if we want 1 job but get many returned we throw valueerror"""
    get_deployed_jobs_mock.return_value = ['k8s/job-asdf', 'k8s/job-jkl;']
    with catch_stdout() as output:
        with pytest.raises(SystemExit):
            get_only_one_job(None, 'too many jobs, pick one')
        output = output.getvalue().strip()
    assert output == "too many jobs, pick one\nJobs to choose from are:\n" + \
        "k8s/job-asdf\nk8s/job-jkl;"


def test_get_only_one_job_job_not_found(get_deployed_jobs_mock):
    """If we request a job with --job-name flag and it doesn't exist"""
    get_deployed_jobs_mock.return_value = ['k8s/job-asdf']
    with catch_stdout() as output:
        with pytest.raises(SystemExit):
            get_only_one_job('not-a-job', '')
        output = output.getvalue().strip()
    assert output == "Job not-a-job not found.\nJobs to choose from are:\n" + \
        'k8s/job-asdf'


def test_get_job_kinds(listdir_mock, open_mock, yaml_load_mock):
    kinds, all_same_kind = get_job_kinds()
    assert kinds == {'the-best-kind'}
    assert all_same_kind is True


def test_get_job_kinds_not_found(listdir_mock):
    listdir_mock.side_effect = FileNotFoundError
    kinds, all_same_kind = get_job_kinds()
    assert kinds is None
    assert all_same_kind is False
