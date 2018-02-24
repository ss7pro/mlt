import json
import os
import sys


class Command(object):
    def __init__(self, args):
        # will store the build and push file json
        self._file_contents = {}
        self.args = args

    def action(self):
        raise NotImplementedError()

    def _fetch_action_arg(self, action, arg):
        action_json = '.{}.json'.format(action)
        # check if we have the json cached or not
        if action_json not in self._file_contents:
            if os.path.isfile(action_json):
                with open(action_json) as f:
                    self._file_contents[action_json] = json.load(f)
        return self._file_contents.get(action_json, {}).get(arg)


class NeedsInitCommand(Command):
    """
    Build, Deploy, Undeploy require being inside a dir that was created
    from Init
    """

    def __init__(self, args):
        self._verify_init()
        self._load_config()
        super(NeedsInitCommand, self).__init__(args)

    def _verify_init(self):
        if not os.path.isfile('mlt.json'):
            print("This command requires you to be in an `mlt init` "
                  "built directory.")
            sys.exit(1)

    # TODO: see if can combine this with _fetch_action_arg
    # to see if it's even necessary to prefetch
    def _load_config(self):
        with open('mlt.json') as f:
            self.config = json.load(f)


class NeedsBuildCommand(Command):
    """We cannot deploy without first having a build"""

    def __init__(self, args):
        super(NeedsBuildCommand, self).__init__(args)
        self._verify_build()

    def _verify_build(self):
        if not os.path.isfile('.build.json'):
            # TODO: see if there's a way to get rid of circular import here
            from mlt.commands.build import Build
            Build(self.args).action()
