import os
from tabulate import tabulate


def parse_templates(templates_directory=None):
    if not templates_directory:
        templates_directory = "/".join(
            [os.path.dirname(__file__), "..", "..", "templates"])

    table = []
    for filename in os.listdir(templates_directory):
        description = ''
        readme_file = templates_directory + "/" + filename + "/README.md"
        if os.path.isfile(readme_file):
            with open(readme_file) as f:
                lines = f.readlines()
                for line in lines:
                    if line[0] == '#' or line[0] == '\n':
                        continue
                    description = line
                    break

        table.append([filename, description])

    return table


def templates_list():
    table = parse_templates()
    print(tabulate(table, headers=['Template',
                                   'Description'], tablefmt="simple"))
