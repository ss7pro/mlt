import os
import json
import time
import uuid
import sys
from string import Template
from subprocess import Popen, PIPE
from termcolor import colored

from . import process_helpers, progress_bar, kubernetes_helpers, build


def deploy(args):
    if not os.path.isfile('.build.json'):
        build.do_build(args)

    do_push(args)

    config = json.load(open('mlt.json'))
    app_name = config['name']
    namespace = config['namespace']

    status = json.load(open('.push.json'))
    remote_container_name = status['last_remote_container']
    run_id = str(uuid.uuid4())

    print("Deploying %s" % remote_container_name)

    # Write new container to deployment
    for filename in os.listdir("k8s-templates"):
        with open('k8s-templates/' + filename) as f:
            deployment_template = f.read()
            s = Template(deployment_template)
            out = s.substitute(image=remote_container_name, app=app_name, run=run_id)

            with open('k8s/' + filename, 'w') as f:
                f.write(out)

        kubernetes_helpers.ensure_namespace_exists(namespace)
        process_helpers.run(["kubectl", "--namespace", namespace, "apply", "-R", "-f", "k8s"])

        print("\nInspect created objects by running:\n  $ kubectl get --namespace=%s all\n" % namespace)


def do_push(args):
    last_push_duration = None
    if os.path.isfile('.push.json'):
        status = json.load(open('.push.json'))
        last_push_duration = status['last_push_duration']

    container_name = None
    if os.path.isfile('.build.json'):
        status = json.load(open('.build.json'))
        container_name = status['last_container']
    else:
        print("Need to run build before pushing")
        sys.exit(1)

    config = json.load(open('mlt.json'))

    is_gke = ('gceProject' in config)

    if is_gke:
        remote_container_name = "gcr.io/" + config['gceProject'] + "/" + container_name
    else:
        remote_container_name = config['registry'] + "/" + container_name

    started_push_time = time.time()
    process_helpers.run(["docker", "tag", container_name, remote_container_name])

    if is_gke:
        push_process = Popen(["gcloud", "docker", "--", "push", remote_container_name], stdout=PIPE, stderr=PIPE)
    else:
        push_process = Popen(["docker", "push", remote_container_name], stdout=PIPE, stderr=PIPE)

    def push_is_done():
        return push_process.poll() is not None
    progress_bar.duration_progress('Pushing ', last_push_duration, push_is_done)
    if push_process.poll() != 0:
        print(colored(push_process.communicate()[0], 'red'))
        sys.exit(1)

    pushed_time = time.time()

    with open('.push.json', 'w') as f:
        f.write(json.dumps({
            "last_remote_container": remote_container_name,
            "last_push_duration": pushed_time - started_push_time
        }))

    print("Pushed to %s" % remote_container_name)
