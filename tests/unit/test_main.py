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
from mock import MagicMock, patch

from mlt.main import run_command

"""
All these tests assert that given a command arg from docopt we call
the right command
"""


@pytest.mark.parametrize('command',
                         ['build', 'deploy', 'init', 'template', 'templates',
                          'undeploy', 'foo'])
def test_run_command(command):
    # couldn't get this to work as a function decorator
    with patch('mlt.main.COMMAND_MAP', ((command, MagicMock()),)) \
            as COMMAND_MAP:
        run_command({command: True})
        COMMAND_MAP[0][1].return_value.action.assert_called_once()