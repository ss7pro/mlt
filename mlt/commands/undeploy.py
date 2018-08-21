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

import json
import os
import subprocess
import sys

from termcolor import colored

from mlt.commands import Command
from mlt.utils import config_helpers, process_helpers, files, sync_helpers


class UndeployCommand(Command):
    def __init__(self, args):
        super(UndeployCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """deletes current kubernetes namespace"""

        if sync_helpers.get_sync_spec() is not None:
            print(colored("This app is currently being synced, please run "
                          "`mlt sync delete` to unsync first", 'red'))
            sys.exit(1)

        namespace = self.config['namespace']

        if files.is_custom('undeploy:'):
            self._custom_undeploy()
        else:
            # don't delete namespace here because we could be using a
            # user-provided namespace
            # can't think of a reason to want to error out mlt if user
            # has undeployed multiple times so ignoring this case for now
            process_helpers.run(
                ["kubectl", "--namespace", namespace, "delete", "-f", "k8s"],
                ignore_failure=True)

    def _custom_undeploy(self):
        """
        Custom undeploy uses the make targets to perform operation.
        """
        if os.path.exists('.push.json'):
            with open('.push.json', 'r') as f:
                data = json.load(f)
        else:
            print("This app has not been deployed yet.")
            sys.exit(1)

        app_run_id = data.get('app_run_id', "")

        if len(app_run_id) < 4:
            print("Something went wrong, "
                  "please delete folder and re-initiate app")
            sys.exit(1)

        job_name = "-".join([self.config['name'], app_run_id])
        # Adding USER env because
        # https://github.com/ksonnet/ksonnet/issues/298
        user_env = dict(os.environ, JOB_NAME=job_name, USER='root')
        try:
            output = subprocess.check_output(["make", "undeploy"],
                                             env=user_env,
                                             stderr=subprocess.STDOUT)
            print(output.decode("utf-8").strip())
        except subprocess.CalledProcessError as e:
            print("Error while undeploying app: {}".format(e.output))
