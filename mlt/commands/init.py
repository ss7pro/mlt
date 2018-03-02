import json
import os
import sys
import shutil
from subprocess import check_output

from mlt import TEMPLATES_DIR
from mlt.commands.base import Command
from mlt.utils import process_helpers


class InitCommand(Command):
    def __init__(self, args):
        super(InitCommand, self).__init__(args)
        self.app_name = self.args["<name>"]

    def action(self):
        """Creates a new git repository based on an mlt template in the
           current working directory.
        """
        template_directory = os.path.join(
            TEMPLATES_DIR, self.args["--template"])

        try:
            shutil.copytree(template_directory, self.app_name)
            data = self._build_mlt_json()
            with open(os.path.join(self.app_name, 'mlt.json'), 'w') as f:
                f.write(json.dump(data, f, indent=2))
            self._init_git_repo()
        except OSError as exc:
            if exc.errno == 17:
                print(
                    "Directory '{}' already exists: delete before trying to "
                    "initialize new application".format(self.app_name))
            else:
                print(exc)

            sys.exit(1)

    def _build_mlt_json(self):
        """generates the data to write to mlt.json"""
        data = {'name': self.app_name, 'namespace': self.app_name}
        if self.args["--registry"] is None:
            raw_project_bytes = check_output(
                ["gcloud", "config", "list", "--format",
                 "value(core.project)"])
            project = raw_project_bytes.decode("utf-8").strip()
            data['gceProject'] = project
        else:
            data['registry'] = self.args["--registry"]
        return data

    def _init_git_repo(self):
        """
        Initialize new git repo in the project dir and commit initial state.
        """
        process_helpers.run(["git", "init", self.app_name])
        process_helpers.run(["git", "add", "."], cwd=self.app_name)
        print(process_helpers.run(
            ["git", "commit", "-m", "Initial commit."], cwd=self.app_name))
