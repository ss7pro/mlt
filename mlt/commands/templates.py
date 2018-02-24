import os
from tabulate import tabulate

from mlt import TEMPLATES_DIR


def parse_templates(templates_directory=TEMPLATES_DIR):
    table = []
    for filename in os.listdir(templates_directory):
        description = ''
        readme_file = os.path.join(templates_directory, filename, "README.md")
        if os.path.isfile(readme_file):
            with open(readme_file) as f:
                for line in f:
                    line = line.strip()
                    if line == '#' or not line:
                        continue
                    description = line
                    break

        table.append([filename, description])

    return table


def templates_list():
    table = parse_templates()
    print(tabulate(table, headers=['Template',
                                   'Description'], tablefmt="simple"))
