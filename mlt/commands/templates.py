import os
from tabulate import tabulate

from mlt import TEMPLATES_DIR
from mlt.commands import Command
from mlt.utils import git_helpers


class TemplatesCommand(Command):
    def action(self):
        """lists templates available"""
        template_repo = self.args["--template-repo"]
        with git_helpers.clone_repo(template_repo) as temp_clone:
            templates_directory = os.path.join(temp_clone, TEMPLATES_DIR)
            templates = self._parse_templates(templates_directory)
        print(tabulate(templates,
                       headers=['Template', 'Description'],
                       tablefmt="simple"))

    def _parse_templates(self, templates_directory):
        result = []
        for filename in os.listdir(templates_directory):
            description = ''
            readme_file = os.path.join(
                templates_directory, filename, "README.md")
            description = '<none>'
            if os.path.isfile(readme_file):
                with open(readme_file) as f:
                    for line in f:
                        line = line.strip()
                        if not line or line[0] == '#':
                            continue
                        description = line
                        break
                result.append([filename, description])
        return result
