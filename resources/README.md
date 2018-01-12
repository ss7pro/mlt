# Resources

## Deploying the TensorFlow operator

This chart is derived from
[tensorflow/k8s](https://github.com/tensorflow/k8s).

```
$ helm install resources/tf-job-operator-chart \
  -n tf-job \
  --wait \
  --replace \
  --set cloud=gke,rbac.install=true,dashboard.install=true,dashboard.serviceType=LoadBalancer
```
