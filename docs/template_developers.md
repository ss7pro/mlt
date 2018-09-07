# Template Developers Manual

The easiest way to add a new template to MLT is to make a copy of one
of the existing templates and then modify it. The following
instructions will go through those steps:

1. Start by making a copy of one of the folders in the `mlt-templates`
 directory.  Either start with something simple like the `hello-world`
 template, or pick a template that is similar to the one that you are
 going to add.

2. Rename the new folder with the name for your template.

3. Update the `README.md` file with a short description of your
template.  Note that this is the description that will be displayed with
`mlt templates list`

4. Other files that typically need to be modified for new templates are:
* `*.py` files
* `requirements.txt` - updated with any libraries that your app uses
* `crd-requirements.txt` - (optional) updated with any operators your model depends on.
By default `crd-check` is performed during the execution of both `mlt init` and `mlt deploy`. The `crd-check` command compares crds specified in crd-requirements.txt against crds in your cluster.
 [Example](../mlt-templates/tf-distributed/crd-requirements.txt)
* `Dockerfile` - modified if the name of the python file to execute is different,
etc.
* `k8s-templates/job.yaml` - required for the kubernetes job, may need to be
modified if a CRD is used, if multiple replicas are needed, or 
if environment variables need to be set, etc.  Note that all files in
the `k8s-templates` directory can have variables like `$app`, `$run`,
and `$image` that will be subbed into the template when the app is
deployed.
* `parameters.json` - (optional) used to define any _additional_ parameters
specific to your template.  These parameters are added to the app's
`mlt.json` file when it's initialized.  The parameter values are subbed
in to the `k8s-templates` directory when the app is deployed.

5. Some templates provide the option to debug unhandled exceptions by
setting a pdb breakpoint and allowing the user to attach into the failed
pod.  Templates that allow this have a `debug_on_fail` option in the
`parameters.json` file. Debugging failures is handled by using the
[kubernetes_debug_wrapper.py](../mlt/utils/kubernetes_debug_wrapper.py)
script.  If a template that includes this option is initailized, the
`kubernetes_debug_wrapper.py` will be copied to the app directory.  As
a template developer, if your app includes this `debug_on_fail` option,
you need to ensure that the entry point in your `Dockerfile` executes
the `kubernetes_debug_wrapper.py` script and passes the model training
script as the next arg:
```
ENTRYPOINT [ "python", "kubernetes_debug_wrapper.py", "main.py" ]
```
Also, the Kubernetes job yaml file needs to have `tty` and `stdin`
enabled for the container and set `DEBUG_ON_FAIL` as an environment
variable:
```
apiVersion: batch/v1
kind: Job
metadata:
  name: $app-$run
spec:
  template:
    spec:
      containers:
      - name: $app
        image: $image
        tty: true
        stdin: true
        env:
        - name: DEBUG_ON_FAIL
          value: '$debug_on_fail'
```

6. To test your template, you need to use the `--template-repo`
parameter with `mlt templates list` and `mlt init` in order
to specify the git url for  template repo (otherwise, this defaults to
`https://github.com/IntelAI/mlt`).

7. For templates supporting `mlt sync`, a few assumptions have been made:
- The Pods for job should either remain running after the job has finished, or the `Job` spec
under `k8s-templates` should contain commented lines describing how to keep the containers running
after the job has finished.
For example here is an snippet from [tf-distributed](../mlt-templates/tf-distributed/k8s-templates/tfjob.yaml)
```aidl
          containers:
            - image: $image
              name: tensorflow
#             ### BEGIN KSYNC SECTION
#             command: ['/bin/sh']
#             args: ['-c', 'python main.py; tail -f /dev/null']
#             ### END KSYNC SECTION
          restartPolicy: OnFailure
```

8. `mlt undeploy` currently assumes all jobs will either be a custom undeploy or a regular undeploy.
It does this by checking if there's a `Makefile` in the template with an `undeploy:` rule.
If you change your app from a normal deploy to a custom deploy, you are required to manually undeploy old jobs using (`kubectl delete deployment/job/...`).
