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
from test_utils.e2e_commands import CommandTester


class UpdateTemplate(CommandTester):
    def test_no_update(self):
        self.init('hello-world')
        # TODO: assert something here
        self.update_template()

    def test_invalid_update(self):
        self.init('hello-world')
        self.config(subcommand="remove", config_name="template_git_sha")
        cmd_output = self.update_template()
        desired_output_string = "ERROR: mlt.json does not have either " \
                                "template_name or template_git_sha. Template" \
                                " update is not possible."
        assert desired_output_string in cmd_output

    @pytest.mark.skip(
        reason="Intermittently failing skipped, for now. Issue - "
               "https://github.com/IntelAI/mlt/issues/288 ")
    def test_valid_update(self):
        self.init('hello-world')
        self.config(subcommand="set", config_name="template_git_sha",
                    config_value="6a5a156196a1cc372bb13dc402fc933a0bb0c5ae")
        cmd_output = self.update_template()
        desired_output_string = "Latest template changes have merged using " \
                                "git, please review change"
        assert desired_output_string in cmd_output
