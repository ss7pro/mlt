# Distributed TensorFlow using Horovod

A distributed model training using horovod and openmpi.

This template deploys horovod model on kubernetes using [kubeflow openmpi](https://github.com/kubeflow/kubeflow/blob/master/kubeflow/openmpi/README.md).

Template structure as follows:

[Dockerfile.cpu](Dockerfile.cpu) - Installs requried packages.
[deploy.sh](deploy.sh) - Custom deployment file which uses kubeflow/openmpi component instructions to deploy on to kubernetes
[exec_multiworker.sh](exec_multiworker.sh) - Entry point in deploy.sh file which initiates the training
[main.py](main.py) - Model file
[parameters.json](parameters.json) - Extra template parameters
[requriemments.txt](requriemments.txt) - Extra python packages
