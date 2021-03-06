#! /bin/bash
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

# check if the service is up and running and get the TB service IP address

if [ ! -z "$( kubectl get service ${JOB_NAME} --namespace ${NAMESPACE} )" ]
then
  ip_address='none'
  timer=0
  # loop until the ip address is assigned to the service or the timer is done.
  while (( timer < 120))
  do
    ip_address=$( kubectl get service ${JOB_NAME} --namespace ${NAMESPACE} -o json | jq -r '.status.loadBalancer.ingress[]?.ip' )
    if [[ ! -z ${ip_address} ]]
    then
        echo "Launching TensorBoard in your local browser..."
        # open TB in the default browser
        open http://${ip_address}:6006
        exit
    fi
    timer=$[$timer+1]
    sleep 5
  done
else
  echo "Cannot open TensorBoard in your local browser, please try 'mlt status' to check if the service is running."
fi
