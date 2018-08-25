#!/bin/bash
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

APP_NAME=kubeflow
# by default we'll use our hyperkube config
# TODO: delete the hyperkube config
# : "${KUBECONFIG:=../resources/config.yaml}"
# workaround for https://github.com/ksonnet/ksonnet/issues/298
export USER=root

# pull ksonnet from web
./scripts/ksonnet_install_linux.sh

# Install kubeflow
export KUBEFLOW_VERSION=0.2.4
wget https://raw.githubusercontent.com/kubeflow/kubeflow/v${KUBEFLOW_VERSION}/scripts/deploy.sh -O deploy.sh

# Disable usage statistics report due to this bug: https://github.com/purpleidea/puppet-gluster/issues/39
sed -i -e 's/ks\ param/#ks\ param/g' deploy.sh
chmod +x deploy.sh
./deploy.sh
pushd
# install Pytorch Operator
ks generate pytorch-operator pytorch-operator
ks apply default -c pytorch-operator
popd
