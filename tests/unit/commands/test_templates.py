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

import os
import pytest
import shutil

from mock import MagicMock
from mlt.commands.templates import TemplatesCommand
from test_utils import project
from test_utils.io import catch_stdout


@pytest.fixture(autouse=True)
def clone_repo_mock(patch):
    clone_mock = MagicMock()
    clone_mock.return_value.__enter__.return_value = 'bar'
    return patch('git_helpers.clone_repo', clone_mock)


@pytest.fixture
def copy_tree_mock(patch):
    return patch('git_helpers.copy_tree')


@pytest.fixture
def open_mock(patch):
    open_mock = MagicMock()
    open_mock.return_value.__enter__.return_value = 'description'
    return patch('open', open_mock)


@pytest.fixture()
def listdir_mock(patch):
    return patch('os.listdir')


@pytest.fixture
def os_path_exists_mock(patch):
    return patch('os.path.exists')


@pytest.fixture
def os_path_isfile_mock(patch):
    return patch('os.path.isfile')


@pytest.fixture
def sorted_mock(patch):
    return patch('sorted')


@pytest.mark.parametrize("valid_template_dir", [
    project.basedir(),
    "git@github.com:IntelAI/mlt.git",
    "https://github.com/IntelAI/mlt",
])
def test_template_list(open_mock, valid_template_dir, copy_tree_mock,
                       listdir_mock, os_path_exists_mock, os_path_isfile_mock,
                       sorted_mock):
    args = {
        'template': 'test',
        'list': True,
        '--template-repo': valid_template_dir
    }
    os_path_exists_mock.return_value = True
    os_path_isfile_mock.return_value = True
    sorted_mock.return_value = ['hello-world', 'tf-dist-mnist']

    templates = TemplatesCommand(args)
    with catch_stdout() as caught_output:
        templates.action()
        assert caught_output.getvalue() is not None


@pytest.mark.parametrize("invalid_template_dir", [
    "/tmp/invalid-mlt-dir",
    "git@github.com:1ntelA1/mlt.git",
    "https://github.com/1ntelA1/mlt",
])
def test_template_list_invalid_repo_dir(invalid_template_dir, copy_tree_mock):
    invalid_template_dir = "/tmp/invalid-mlt-dir"
    args = {
        'template': 'test',
        'list': True,
        '--template-repo': invalid_template_dir
    }

    if invalid_template_dir.startswith("/tmp/"):
        if os.path.exists(invalid_template_dir):
            shutil.rmtree(invalid_template_dir)

    templates = TemplatesCommand(args)
    with catch_stdout() as caught_output:
        templates.action()
        assert caught_output.getvalue() is not None
