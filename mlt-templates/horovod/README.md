# Distributed TensorFlow using Horovod

A distributed model training using horovod and openmpi.

This template deploys horovod model on kubernetes using [kubeflow openmpi](https://github.com/kubeflow/kubeflow/blob/master/kubeflow/openmpi/README.md).

Template structure as follows:

* [Dockerfile.cpu](Dockerfile.cpu) - Installs requried packages.
* [deploy.sh](deploy.sh) - Custom deployment file which uses kubeflow/openmpi component instructions to deploy on to kubernetes
* [exec_multiworker.sh](exec_multiworker.sh) - Entry point in deploy.sh file which initiates the training
* [main.py](main.py) - Model file
* [parameters.json](parameters.json) - Extra template parameters
* [requriements.txt](requriemments.txt) - Extra python packages


## How to create horovod template
`mlt init --template=horovod --registry={gcr.io/<project_id> or docker.io/<dockeruser-id>} <name_as_you_like>`


## Volume support

We have volume support in our template where you can mount `hostpath` on your kubernetes node as volume inside containers.
We have used [vck](https://github.com/IntelAI/vck/blob/master/docs/ops.md#installing-the-controller) to  transfer data to kubernetes cluster.

Please update below paths in `mlt.json`(this file will be created after `mlt init`)
* `data_path` - Path to training data (.npy files in our case)
* `output_path` - Sub-directory inside the mounted volume to store results. You can use this path to check your results after training finishes.

In case of this `mnist` example, data will be downloaded inside containers if provided path is not valid.
