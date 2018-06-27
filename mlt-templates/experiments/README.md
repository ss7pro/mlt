# MLT Experiments Application

Runs hyperparameter experiments for a demo job.

This template uses code from the [experiments](https://github.com/intelai/experiments)
repository and requires that the `experiments.ml.intel.com` and
`results.ml.intel.com` CRDs are installed on the cluster.  Your namespace
must also be setup with the proper [permissions/roles](https://github.com/IntelAI/experiments/blob/master/examples/demo/sa.yaml)
for using the experiments and results CRDs and to allow the optimizer
job to create new jobs for each experiment.
