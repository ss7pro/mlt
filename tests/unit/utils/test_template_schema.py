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
import os
from jsonschema import ValidationError

import mlt.utils.schema as schema


def test_invalid_yaml():
    cwd = os.getcwd()
    os.chdir("tests/unit/utils/sample-templates/invalid-template")
    with pytest.raises(ValidationError):
        schema.validate()
    os.chdir(cwd)


def test_valid_yaml():
    cwd = os.getcwd()
    os.chdir("tests/unit/utils/sample-templates/valid-template")
    output = schema.validate()
    assert output is None
    os.chdir(cwd)


def test_yaml_with_multiple_doc():
    cwd = os.getcwd()
    os.chdir("tests/unit/utils/sample-templates/multiple_doc_template")
    output = schema.validate()
    assert output is None
    os.chdir(cwd)
