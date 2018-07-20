# TensorBoard MLT Application for Bare Metal Clusters

A TensorBoard service in Kubernetes Bare Metal cluster.

This template requires the path to the TensorFlow job logs and the user domain to be configured.
The command below shows how to update the log directory value in `k8s-templates/tbjob.yaml`.

`mlt config set template_parameters.logdir <value>` , and
`mlt config set template_parameters.domain <value>`

TensorBoard template works with different storage sources, and it's the user responsibility to allow the TensorBoard service to access the logs location.

This template assumes that `jq` is installed. `jq` is used while launching TensorBoard to query the service host.

### Steps to launch TensorBoard service using TensorBoard MLT template:

1. Create a TensorBoard application using the TensorBoard MLT template.
`mlt init tensorboard-app --template=tensorboard-bm --namespace=<value> --registry-<value>`

From inside the application `cd tensorboard-app` :

2. Set TensorBoard `logdir` and `domain`.
`mlt config set template_parameters.logdir <value>` and
`mlt config set template_parameters.domain <value>`

3. Create the application image.
`mlt build`

4. Deploy TensorBoard service.
`mlt deploy`,
which deploys the TensorBoard service and launches the local browser with `http://<service-name>.domain`.

7. Finally, when done, a user can delete the running TensorBoard service
`mlt undeploy`.
