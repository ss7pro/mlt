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

import yaml
import glob
import jsonschema

schema = """
---
type: object
required:
- apiVersion
- kind
- metadata
- spec
properties:
  apiVersion:
    type: string
  kind:
    type: string
  metadata:
    type: object
    required:
    - name
    properties:
      name:
        type: string
  spec:
    type: object
    properties:
      group:
        type: string
      version:
        type: string
      scope:
        type: string
        enum:
        - Namespaced
        - Cluster
      names:
        type: object
        required:
        - plural
        - singular
        - kind
        - shortNames
        properties:
          plural:
            type: string
          singular:
            type: string
          kind:
            type: string
          shortNames:
            type: array
            items:
              type: string
"""


def validate():
    """ Validates template yamls in <app>/k8s-templates directory.
        Raises ValidationError on invalid yaml """
    for template_yaml in glob.glob("k8s-templates/*.yaml"):
        with open(template_yaml) as template:
            docs = yaml.load_all(template)
            for doc in docs:
                jsonschema.validate(doc, yaml.load(schema))
