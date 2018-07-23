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
from subprocess import CalledProcessError

from test_utils import project
from test_utils.io import catch_stdout
from mlt.commands.update_template import UpdateTemplateCommand


@pytest.fixture
def chdir(patch):
    return patch('os.chdir')


@pytest.fixture
def copy_tree_mock(patch):
    return patch('copy_tree')


@pytest.fixture
def ospath_exists(patch):
    return patch('os.path.exists')


@pytest.fixture
def verify_init(patch):
    return patch('config_helpers.load_config')


@pytest.fixture
def get_latest_sha(patch):
    return patch('git_helpers.get_latest_sha',
                 MagicMock(return_value="abcdefg"))


@pytest.fixture()
def git_clone(patch):
    clone_mock = MagicMock()
    clone_mock.return_value.__enter__.return_value = 'bar'
    return patch('git_helpers.clone_repo', clone_mock)


@pytest.fixture
def process_helpers(patch):
    return patch('process_helpers')


def test_invalid_config(verify_init, process_helpers, git_clone,
                        ospath_exists):
    args = {
        'template': 'test',
        '--template-repo': project.basedir(),
        'update-template': True
    }
    update_template = UpdateTemplateCommand(args)
    update_template.config = {'template_git_sha': 'abcdefg',
                              'name': 'testapp'}
    error_string = "ERROR: mlt.json does not have either template_name " \
                   "or template_git_sha."
    with catch_stdout() as caught_output:
        update_template.action()
        assert error_string in caught_output.getvalue()

    update_template.config = {'template_name': 'test', 'name': 'testapp'}
    error_string = "ERROR: mlt.json does not have either template_name " \
                   "or template_git_sha."
    with catch_stdout() as caught_output:
        update_template.action()
        assert error_string in caught_output.getvalue()


def test_no_update(verify_init, process_helpers, git_clone,
                   chdir, get_latest_sha, ospath_exists):
    args = {
        'template': 'test',
        '--template-repo': project.basedir(),
        'update-template': True
    }
    update_template = UpdateTemplateCommand(args)
    update_template.config = {'template_git_sha': 'abcdefg',
                              'name': 'testapp',
                              'template_name': 'test'}
    noupdate_string = "Template is up to date, no need for update."
    with catch_stdout() as caught_output:
        update_template.action()
        assert noupdate_string in caught_output.getvalue()


def test_unable_to_update(verify_init, git_clone, copy_tree_mock,
                          ospath_exists, chdir):
    template_name = 'testapp'
    args = {
        'template': template_name,
        '--template-repo': project.basedir(),
        'update-template': True
    }
    ospath_exists.return_value = False
    update_template = UpdateTemplateCommand(args)
    update_template.config = {'template_git_sha': 'abcdefg',
                              'name': template_name,
                              'template_name': template_name}
    with catch_stdout() as caught_output:
        update_template.action()
        assert caught_output.getvalue().strip() == "Unable to update, "\
            "template {} does not exist in MLT git repo.".format(template_name)


def test_unable_to_git_pull_master(verify_init, copy_tree_mock, chdir,
                                   process_helpers, git_clone, ospath_exists):
    """we'll hit CalledProcessError to assert that git pull origin master
       failed
    """
    template_name = 'testapp'
    args = {
        'template': template_name,
        '--template-repo': project.basedir(),
        'update-template': True
    }
    process_helpers.run.side_effect = [
        '', '', '', CalledProcessError(0, 'error', 'error')]
    update_template = UpdateTemplateCommand(args)
    update_template.config = {'template_git_sha': 'abcdefg',
                              'name': template_name,
                              'template_name': template_name}
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            update_template.action()
        assert 'error' in caught_output.getvalue().strip()


def test_valid_case(verify_init, copy_tree_mock, process_helpers, git_clone,
                    chdir, get_latest_sha, ospath_exists):
    args = {
        'template': 'test',
        '--template-repo': project.basedir(),
        'update-template': True
    }
    update_template = UpdateTemplateCommand(args)
    update_template.config = {'template_git_sha': 'pqrs',
                              'name': 'testapp',
                              'template_name': 'test'}
    update_string = "Latest template changes have merged using git"
    with catch_stdout() as caught_output:
        update_template.action()
        assert update_string in caught_output.getvalue()
