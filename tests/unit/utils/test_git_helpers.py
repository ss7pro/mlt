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

from mlt.utils import git_helpers


@pytest.fixture
def contextmanager_mock(patch):
    return patch('contextmanager')


@pytest.fixture
def chdir_mock(patch):
    return patch('os.chdir')


@pytest.fixture
def os_path_exists_mock(patch):
    return patch('os.path.exists')


@pytest.fixture
def copy_tree_mock(patch):
    return patch('copy_tree')


@pytest.fixture
def is_git_repo_mock(patch):
    return patch('is_git_repo')


@pytest.fixture
def run_mock(patch):
    return patch('process_helpers.run')


@pytest.fixture
def run_popen_mock(patch):
    return patch('process_helpers.run_popen')


@pytest.fixture
def shutil_mock(patch):
    return patch('shutil')


@pytest.fixture
def tempfile_mock(patch):
    return patch('tempfile')


@pytest.mark.parametrize('git_repo', [True, False])
def test_clone_repo(contextmanager_mock, copy_tree_mock, is_git_repo_mock,
                    os_path_exists_mock, run_popen_mock, shutil_mock,
                    tempfile_mock, git_repo):
    is_git_repo_mock.return_value = git_repo
    os_path_exists_mock.return_value = True

    with git_helpers.clone_repo('hello-world'):
        # hack to get the contextmanager func called
        pass
    run_popen_mock.return_value.wait.assert_called_once()
    if not git_repo:
        copy_tree_mock.assert_called_once()


def test_get_latest_sha(chdir_mock, run_mock):
    run_mock.return_value = 'nsdf923r89fwejks\n'
    assert git_helpers.get_latest_sha('hello-world') == 'nsdf923r89fwejks'


@pytest.mark.parametrize("template_repo,is_git", [
    ("git@github.com:IntelAI/mlt.git", True),
    ("https://github.com/IntelAI/mlt.git", True),
    (".", False),
    ("/home/user/mlt", False)
])
def test_is_git_repo(template_repo, is_git):
    assert git_helpers.is_git_repo(template_repo) == is_git


def test_get_experiments_version():
    """ Ensure we get a non-empty experiments version """
    version = git_helpers.get_experiments_version()
    assert version
