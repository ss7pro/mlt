import json
import os
import sys


def load_config():
    """stores mlt.json data in self.config"""
    if os.path.isfile('mlt.json'):
        with open('mlt.json') as f:
            return json.load(f)
    else:
        print("This command requires you to be in an `mlt init` "
              "built directory.")
        sys.exit(1)
