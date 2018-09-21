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

FROM python:3.6.6

RUN apt-get update && apt-get install -y git

ADD requirements.txt /src/deps/requirements.txt
RUN pip install -r /src/deps/requirements.txt

# Install MKL optimized tensorflow.
ADD tensorflow-1.9.0-cp36-cp36m-linux_x86_64.whl /src/deps/tensorflow-1.9.0-cp36-cp36m-linux_x86_64.whl

RUN pip install --upgrade pip && \
    pip install /src/deps/tensorflow-1.9.0-cp36-cp36m-linux_x86_64.whl

WORKDIR /src/app

ADD . /src/app

RUN chmod +x run_benchmarks.sh

ENTRYPOINT ["./run_benchmarks.sh", "/home/nfsshare/unet/2016_dataset", "/home/nfsshare/unet/2016_dataset/single-node/checkpoints"]