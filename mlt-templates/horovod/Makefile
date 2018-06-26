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

.PHONY: dependencies

SHELL := /bin/bash

all: main

main: main.py
	@echo "Should run linting and tests before submitting application"

build:
	@if [ "${GPUS}" == 0 ]; then \
	    docker build --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --target=ubuntu_cpu -t ${CONTAINER_NAME} -f Dockerfile.cpu . ; \
	else \
	    docker build --build-arg HTTP_PROXY=${HTTP_PROXY} --build-arg HTTPS_PROXY=${HTTPS_PROXY} --build-arg http_proxy=${http_proxy} --build-arg https_proxy=${https_proxy} --target=ubuntu_gpu -t ${CONTAINER_NAME} -f Dockerfile.gpu . ; \
	fi;

deploy:
	@chmod +x deploy.sh
	@GITHUB_TOKEN=${GITHUB_TOKEN} ./deploy.sh

undeploy:
	@if [ -d ${JOB_NAME} ]; then \
		cd ${JOB_NAME} && ks delete default ; \
		ks component rm ${JOB_NAME} ; \
		cd - ; \
		rm -rf ${JOB_NAME} ; \
	else \
		echo "Job not yet deployed" ; \
	fi;

status:
	@kubectl get pods --namespace ${NAMESPACE} -o wide -a -l app=${JOB_NAME}
