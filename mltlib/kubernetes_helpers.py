import os
from subprocess import call

from . import process_helpers

def ensure_namespace_exists(ns):
    exit_code = call(["kubectl", "get", "namespace", ns], stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
    if exit_code is not 0:
        process_helpers.run(["kubectl", "create", "namespace", ns])