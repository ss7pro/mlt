# TensorBoard MLT Application

A TensorBoard service in Kubernetes cluster.

This template requires the path to the TensorFlow job logs to be configured.
The command below shows how to update the log directory value in `k8s-templates/tbjob.yaml`.

`mlt config set template_parameters.logdir <value>`

TensorBoard template works with different storage sources, and it's the user responsibility to allow the TensorBoard service to access the logs location.

This template assumes that Ingress controller is enabled in the Kubernetes cluster. 



## Example: Using the TensorBoard template with Google Cloud Storage

- When using Google Kubernetes Engine (GKE) (similar to this example), installing Ingress is not needed as GKE can expose Kubernetes services using [GCP load balancer](https://cloud.google.com/kubernetes-engine/docs/how-to/exposing-apps).

- Assuming that the user stores TensorFlow jobs logs/results in gcloud storage as S3 bucket, then the 'logdir' value would be 
`S3://<user-bucket-name>/<directory-name>`. In this case, to allow access to the storage source, the user gets the access key and ID from gcloud storage and use them to create `gcs-creds` secrets in `kubectl`:

```
GCS_ACCESS_KEY_ID=user-access-key-id-value
GCS_SECRET_ACCESS_KEY=user-secret-access-key-value
kubectl create secret generic gcs-creds --from-literal=awsAccessKeyID=${GCS_ACCESS_KEY_ID} \
 --from-literal=awsSecretAccessKey=${GCS_SECRET_ACCESS_KEY}
 ```

### Steps to launch TensorBoard service using TensorBoard MLT template:

1. Create a TensorBoard application using the TensorBoard MLT template.
`mlt init tensorboard-app --template=tensorboard`

From inside the application `cd tensorboard-app` :

2. Set TensorBoard `logdir`.
`mlt config set template_parameters.logdir S3://<user-bucket-name>/<directory-name>`

3. Create the application image.
`mlt build`

In this example, the user need to modify k8s-templates/tbjob.yaml to add the previously created secrets, as follows:

```
          env:
          - name: AWS_ACCESS_KEY_ID
            valueFrom:
              secretKeyRef:
                name: gcs-creds
                key: awsAccessKeyID
          - name: AWS_SECRET_ACCESS_KEY
            valueFrom:
              secretKeyRef:
                name: gcs-creds
                key: awsSecretAccessKey
          - name: AWS_REGION
            value: "us-west-1"
          - name: S3_REGION
            value: "us-west-1"
          - name: S3_USE_HTTPS
            value: "true"
          - name: S3_VERIFY_SSL
            value: "true"
          - name: S3_ENDPOINT
            value: "storage.googleapis.com"
```

4. Deploy TensorBoard service.
`mlt deploy`,
which deploys the TensorBoard service and launches the local browser with `http://<EXTERNAL-IP>:6006`.

7. Finally, when done, a user can delete the running TensorBoard service
`mlt undeploy`.
