# Distributed TensorFlow using Horovod

A distributed model training using horovod and openmpi.

This template deploys horovod model on kubernetes using [kubeflow openmpi] (https://github.com/kubeflow/kubeflow/blob/master/kubeflow/openmpi/README.md).

Template structure as follows:

* deploy.sh - Actual script which deploys your model to k8.
* Dockerfile.cpu - Used when `gpus=0`
* Dockerfile.gpu - Used when `gpus > 0`
* main.py - Sample tensorflow_mnist model using horovod. (Replace content in this file with your own model content. *Note:* do not change filename)
* Makefile - Contains targets for your template
* requirements.txt - List tensorflow versions you want to use (Make sure to use right Nvidia/Cuda versions
        because they are tightly coupled with tensorflow version)
