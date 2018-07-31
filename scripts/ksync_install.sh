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

# This is script should run only after a kubectl context has been established
export TARGET_INSTALL_PATH=$HOME/.ksync/bin
if [ ! -d ${TARGET_INSTALL_PATH} ]; then
    mkdir -p ${TARGET_INSTALL_PATH}
fi

HOST_OS=${HOST_OS:-$(uname | tr '[:upper:]' '[:lower:]')}
if [[ $(uname -m) == "x86_64" ]]; then
  HOST_ARCH="amd64"
else
  HOST_ARCH=${HOST_ARCH:-$(uname -m)}
fi

KSYNC_TAG=0.3.1
wget --quiet https://github.com/vapor-ware/ksync/releases/download/$KSYNC_TAG/ksync_${HOST_OS}_${HOST_ARCH} \
    -O $TARGET_INSTALL_PATH/ksync

export KSYNC="$HOME/.ksync/bin/ksync"
chmod +x $KSYNC

USER_SHELL=$(echo ${SHELL##*/})
if [[ $USER_SHELL = *"bash"* ]]; then
    grep -q -F 'export PATH=$PATH:$HOME/.ksync/bin' "$HOME/.bashrc" || echo 'export PATH=$PATH:$HOME/.ksync/bin' >> "$HOME/.bashrc"
    source $HOME/.bashrc
else
    echo "ksync is installed at $KSYNC. Please update your PATH accordingly."
fi

# Initialize Ksync and run the ksync watch and doctor
$KSYNC init

for i in {1..60}; do
    KSYNC_PODS_COUNT=$(kubectl get pods -n kube-system -l app=ksync | grep Running | wc -l)
    CLUSTER_NODE_COUNT=$(kubectl get nodes | grep Ready | wc -l)
    if ! pgrep -x "ksync" > /dev/null; then
        echo "Running ksync in daemon mode"
        $KSYNC watch -d
        sleep 5
    fi
    if [ $KSYNC_PODS_COUNT -eq $CLUSTER_NODE_COUNT ]; then
        echo "Ksync is installed successfully"
        echo "Running ksync health checker now"
        $KSYNC doctor
        exit 0
    else
        echo "Ksync pods are being created";
        sleep 10
    fi
done

echo "Ksync failed to be installed or user does not have proper permissions to check the installation"
exit 1

