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
import sys
from subprocess import check_output, CalledProcessError, Popen, PIPE


def run(command, cwd=None, raise_on_failure=False, ignore_failure=False):
    """wrapper around check_output call
       raise_on_failure: mlt will raise error if output call failed
       ignore_failure: mlt won't even print out any error that occurred
                       (useful for mlt undeploy call, in case undeploy
                        was called multiple times for some reason)
    """
    output = ''
    try:
        output = check_output(command, cwd=cwd).decode("utf-8")
    except CalledProcessError as e:
        if raise_on_failure:
            raise e
        if not ignore_failure:
            print(e.output)
            sys.exit(1)

    return output


def run_popen(command, shell=False, stdout=PIPE, stderr=PIPE, cwd=None,
              preexec_fn=None):
    """to suppress output, pass False to stdout or stderr
       None is a valid option that we want to allow"""
    with open(os.devnull, 'w') as quiet:
        stdout = quiet if stdout is False else stdout
        stderr = quiet if stderr is False else stderr
        if not (isinstance(command, str) or isinstance(command, list)):
            print("The following command is invalid:\n{}".format(command))
            sys.exit(1)
        try:
            return Popen(command, stdout=stdout, stderr=stderr, shell=shell,
                         cwd=cwd, preexec_fn=preexec_fn)
        except CalledProcessError as e:
            print(e.output)
            sys.exit(1)
