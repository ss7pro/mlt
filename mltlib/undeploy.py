import os
import sys
import json

from . import process_helpers


def undeploy(args):
    if not os.path.isfile('.studio.json'):
        print("run `mlt undeploy` within a project directory")
        sys.exit(1)

    config = json.load(open('.studio.json'))
    namespace = config['namespace']
    process_helpers.run(["kubectl", "--namespace", namespace, "delete", "-f", "k8s"])
