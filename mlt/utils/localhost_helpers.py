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


def binary_path(binary="docker"):
    """
    checks if executable 'binary' exists in PATH
    :param binary: executable name to be searched for
    :return: full path to 'binary' or None if not in PATH
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(binary)
    if fpath:
        if is_exe(binary):
            return binary
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, binary)
            if is_exe(exe_file):
                return exe_file

    return None
