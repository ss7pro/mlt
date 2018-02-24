import os
import json
import time
import uuid
import sys
from string import Template
from subprocess import Popen, PIPE
from termcolor import colored

from mlt.commands import NeedsInitCommand, NeedsBuildCommand
from mlt.utils import process_helpers, progress_bar, kubernetes_helpers


class Deploy(NeedsInitCommand, NeedsBuildCommand):
    def action(self):
        self._push()

        app_name = self.config['name']
        namespace = self.config['namespace']

        remote_container_name = self._fetch_action_arg(
            'push', 'last_remote_container')

        print("Deploying {}".format(remote_container_name))

        # Write new container to deployment
        for filename in os.listdir("k8s-templates"):
            with open(os.path.join('k8s-templates', filename)) as f:
                template = Template(f.read())
                out = template.substitute(image=remote_container_name,
                                          app=app_name, run=str(uuid.uuid4()))

                with open(os.path.join('k8s', filename), 'w') as f:
                    f.write(out)

            kubernetes_helpers.ensure_namespace_exists(namespace)
            process_helpers.run(
                ["kubectl", "--namespace", namespace, "apply", "-R",
                 "-f", "k8s"])

            print("\nInspect created objects by running:\n"
                  "$ kubectl get --namespace={} all\n".format(namespace))

    def _push(self):
        last_push_duration = self._fetch_action_arg(
            'push', 'last_push_duration')
        self.container_name = self._fetch_action_arg(
            'push', 'last_container')

        if 'gceProject' in self.config:
            self._push_gke()
        else:
            self._push_docker()

        progress_bar.duration_progress(
            'Pushing ', last_push_duration,
            lambda: self.push_process.poll() is not None)
        if self.push_process.poll() != 0:
            print(colored(self.push_process.communicate()[0], 'red'))
            sys.exit(1)

        with open('.push.json', 'w') as f:
            f.write(json.dumps({
                "last_remote_container": self.remote_container_name,
                "last_push_duration": time.time() - self.started_push_time
            }))

        print("Pushed to {}".format(self.remote_container_name))

    def _push_gke(self):
        self.remote_container_name = "gcr.io/" + \
            self.config['gceProject'] + "/" + self.container_name
        self._start_push_time_and_tag()
        self.push_process = Popen(["gcloud", "docker", "--", "push",
                                   self.remote_container_name],
                                  stdout=PIPE, stderr=PIPE)

    def _push_docker(self):
        self.remote_container_name = self.config['registry'] + \
            "/" + self.container_name
        self._start_push_time_and_tag()
        self.push_process = Popen(
            ["docker", "push", self.remote_container_name],
            stdout=PIPE, stderr=PIPE)

    def _start_push_time_and_tag(self):
        self.started_push_time = time.time()
        process_helpers.run(
            ["docker", "tag", self.container_name, self.remote_container_name])
