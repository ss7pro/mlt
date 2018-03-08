import os
from tabulate import tabulate

from mlt import TEMPLATES_DIR
from mlt.commands import Command


class TemplatesCommand(Command):
    def action(self):
        """lists templates available"""
        self._parse_templates()
        print(tabulate(self.table,
                       headers=['Template', 'Description'],
                       tablefmt="simple"))

    def _parse_templates(self, templates_directory=TEMPLATES_DIR):
        self.table = []
        for filename in os.listdir(templates_directory):
            description = ''
            readme_file = os.path.join(
                templates_directory, filename, "README.md")
            if os.path.isfile(readme_file):
                with open(readme_file) as f:
                    for line in f:
                        line = line.strip()
                        if line == '#' or not line:
                            continue
                        description = line
                        break
                self.table.append([filename, description])
