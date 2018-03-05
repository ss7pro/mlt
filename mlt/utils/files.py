import json
import os


def fetch_action_arg(action, arg):
    """fetches data from command json files"""
    action_json = '.{}.json'.format(action)
    if os.path.isfile(action_json):
        with open(action_json) as f:
            return json.load(f).get(arg)
