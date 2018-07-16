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


from mlt.utils.process_helpers import run
from test_utils.e2e_commands import CommandTester


# NOTE: you need to deploy first before you deploy with --no-push
# otherwise you have no image to use to make new container from


class TestDeployFlow(CommandTester):
    @pytest.fixture(autouse=True, scope='function')
    def teardown(self):
        """Allow normal deployment, then undeploy and check status at end of
           every test. Also delete the namespace because undeploy doesn't
           do that.
           NOTE: is there a better way to write this? :joy:
        """
        try:
            # normal test execution
            yield
        finally:
            # no matter what, undeploy and check status
            try:
                self.undeploy()
                self.status()
            finally:
                # tear down namespace at end of test
                try:
                    run(["kubectl", "delete", "ns", self.namespace])
                except SystemExit:
                    # this means that the namespace and k8s resources are
                    # already deleted or were never created
                    pass

    @pytest.mark.parametrize('template',
                             filter(lambda x: os.path.isdir(
                                 os.path.join('mlt-templates', x)),
                                 os.listdir('mlt-templates')))
    def test_deploying_templates(self, template):
        self.init(template)
        self.build()
        self.deploy()
        self.status()

    def test_deploy_enable_sync(self):
        self.init(enable_sync=True)
        self.build()
        self.deploy(sync=True)
        self.sync(create=True)
        self.status()
        self.sync(reload=True)
        self.status()
        self.sync(delete=True)

    def test_no_push_deploy(self):
        self.init()
        self.build()
        self.deploy()
        self.status()
        self.deploy(no_push=True)
        self.status()

    def test_interactive_deploy(self):
        self.init()
        self.build()
        self.deploy()
        self.status()
        self.deploy(interactive=True, no_push=True, retries=60)
        self.status()

    def test_watch_build_and_deploy_no_push(self):
        self.init()
        self.build(watch=True)
        self.deploy()
        self.status()
        self.deploy(no_push=True)
        self.status()
