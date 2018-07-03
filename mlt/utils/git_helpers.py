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
import shutil
import tempfile
from contextlib import contextmanager
from distutils.dir_util import copy_tree

from mlt.utils import process_helpers


@contextmanager
def clone_repo(repo):
    destination = tempfile.mkdtemp()
    process_helpers.run_popen(
        "git clone {} {}".format(repo, destination),
        shell=True, stdout=False, stderr=False).wait()

    # If the template repo is a local path, then copy the local directory over
    # the git clone so that the templates reflect the local changes.
    if not is_git_repo(repo):
        copy_tree(repo, destination)

    try:
        yield destination
    finally:
        # This is really a bug in 'shutil' as described here:
        # https://bugs.python.org/issue29699
        # Also the option ignore_errors is set to True mainly for Unit tests:
        # https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
        if os.path.exists(destination):
            shutil.rmtree(destination, ignore_errors=True)


def get_latest_sha(repo):
    """ Returns latest git sha of given git repo directory. """
    cwd = os.getcwd()
    command = "git rev-list -1 HEAD -- {0}".format(repo)
    os.chdir(repo)
    git_sha = process_helpers.run(command.split(" "))
    os.chdir(cwd)
    return git_sha.strip()


def is_git_repo(template_repo):
    """ Returns True if the template_repo looks like a git repository. """
    return template_repo.startswith("git@") or \
        template_repo.startswith("https://")


def get_experiments_version():
    """ Returns the git version of the experiments repo to use """
    with open("mlt-templates/experiments/EXPERIMENTS_VERSION.txt", "r") as fh:
        experiments_version = fh.read()
    return experiments_version
