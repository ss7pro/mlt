# UNET single node

These scripts help in running unet single node training both on k8 and bare metal.

## Kubernetes
It's just the same way of deploying `mlt` app.
* `mlt build` - To build image. Use `mlt build -v` to see verbose
* `mlt deploy`- Pushes to given registry and then deploys on to kubernetes

## Bare metal

Script expects to pass training data folder, output folder and conda environment to use.

`./run_benchmarks.sh <path_to_training_data> <path_to_subfolder_within_training_data> <conda_env_name>`

```
./run_benchmarks.sh /home/nfsshare/unet/2016_dataset /home/nfsshare/unet/2016_dataset/single-node-bm/checkpoints tf_19_cnn_horovod

```

