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
from test_utils.e2e_commands import CommandTester
from test_utils.files import create_work_dir


def test_no_update():
    with create_work_dir() as workdir:
        commands = CommandTester(workdir)
        commands.init('hello-world')
        commands.update_template()


def test_invalid_update():
    with create_work_dir() as workdir:
        commands = CommandTester(workdir)
        commands.init('hello-world')
        new_config = "template_git_sha"
        commands.config(subcommand="remove", config_name=new_config)
        cmd_output = commands.update_template()
        desired_output_string = 'ERROR: mlt.json does not have either template_name' \
                                ' or template_git_sha. Template update is not possible.'
        assert desired_output_string in cmd_output


def test_valid_update():
    with create_work_dir() as workdir:
        commands = CommandTester(workdir)
        commands.init('hello-world')
        new_config = "template_git_sha"
        new_value = "6a5a156196a1cc372bb13dc402fc933a0bb0c5ae"
        commands.config(subcommand="set", config_name=new_config,
                        config_value=new_value)
        cmd_output = commands.update_template()
        desired_output_string = 'Latest template changes have merged using git, ' \
                                'please review change'
        assert desired_output_string in cmd_output

