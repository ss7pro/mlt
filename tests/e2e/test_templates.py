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
from subprocess import check_output
from test_utils import project

from mlt.utils import constants, git_helpers
from test_utils.e2e_commands import CommandTester


class TestTemplates(CommandTester):
    def _call_template_list(self, template_repo):
        return check_output(['mlt', 'templates', 'list',
                             '--template-repo={}'.format(template_repo)]
                            ).decode("utf-8")

    def test_templates(self):
        output = self._call_template_list(project.basedir())
        desired_template_output = """Template             Description
-------------------  ---------------------------------------------------------\
-----------------------------------------
experiments          Runs hyperparameter experiments for a demo job.
hello-world          A TensorFlow python HelloWorld example run through \
Kubernetes Jobs.
horovod              A distributed model training using horovod and openmpi.
pytorch              Sample distributed application taken from \
http://pytorch.org/tutorials/intermediate/dist_tuto.html
pytorch-distributed  A distributed PyTorch MNIST example run using the \
pytorch-operator.
tensorboard-bm       A TensorBoard service in Kubernetes Bare Metal cluster.
tensorboard-gke      A TensorBoard service in Google Kubernetes cluster.
tf-dist-mnist        A distributed TensorFlow MNIST model which designates \
worker 0 as the chief.
tf-distributed       A distributed TensorFlow matrix multiplication run \
through the TensorFlow Kubernetes Operator.
"""

        assert output == desired_template_output

    def test_local_templates(self):
        """
        Tests creating a new template in a clone of mlt.  Verifies that we can
        specify the template-repo for mlt template list and see new template in
        the list.  Then uses mlt init to create an app with new template and
        verifies that the app directory exists.
        """
        # Create a git clone of mlt to use as a local template diretory
        with git_helpers.clone_repo(project.basedir()) as temp_clone:
            # Add a new test template to the local mlt template directory
            templates_directory = os.path.join(
                temp_clone, constants.TEMPLATES_DIR)
            new_template_name = "test-local"
            new_template_directory = os.path.join(templates_directory,
                                                  new_template_name)
            os.mkdir(new_template_directory)
            new_template_file = os.path.join(
                new_template_directory, "README.md")
            with open(new_template_file, "w") as f:
                f.write("New local template for testing")

            # call mlt template list and then check the output
            output = self._call_template_list(temp_clone)

            # template list should include our new test-local template
            desired_template_output = """Template             Description
-------------------  ---------------------------------------------------------\
-----------------------------------------
experiments          Runs hyperparameter experiments for a demo job.
hello-world          A TensorFlow python HelloWorld example run through \
Kubernetes Jobs.
horovod              A distributed model training using horovod and openmpi.
pytorch              Sample distributed application taken from \
http://pytorch.org/tutorials/intermediate/dist_tuto.html
pytorch-distributed  A distributed PyTorch MNIST example run using the \
pytorch-operator.
tensorboard-bm       A TensorBoard service in Kubernetes Bare Metal cluster.
tensorboard-gke      A TensorBoard service in Google Kubernetes cluster.
test-local           New local template for testing
tf-dist-mnist        A distributed TensorFlow MNIST model which designates \
worker 0 as the chief.
tf-distributed       A distributed TensorFlow matrix multiplication run \
through the TensorFlow Kubernetes Operator.
"""
            assert output == desired_template_output

            # init an app with this new template and verify that the app exists
            self.init(template=new_template_name, template_repo=temp_clone)
            assert os.path.isdir(self.project_dir)
            assert os.path.isfile(os.path.join(
                self.project_dir, "README.md"))
