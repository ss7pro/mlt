#!/usr/bin/env python
"""mlt.
Usage:
  mlt (-h | --help)
  mlt --version
  mlt init [--template=<template>] [--registry=<registry>] <name>
  mlt build [--watch]
  mlt deploy
  mlt undeploy
  mlt (template | templates) list

Options:
  --template=<template> Template name for app
                        initialization [default: hello-world].
  --registry=<registry> Container registry to use.
                        If none is set, will attempt to use gcloud.
"""
import os

from docopt import docopt

from mlt.commands import (BuildCommand, DeployCommand, InitCommand,
                          TemplatesCommand, UndeployCommand)

# every available command and its corresponding action will go here
COMMAND_MAP = (
    ('build', BuildCommand),
    ('deploy', DeployCommand),
    ('init', InitCommand),
    ('template', TemplatesCommand),
    ('templates', TemplatesCommand),
    ('undeploy', UndeployCommand),
)


def run_command(args):
    """maps params from docopt into mlt commands"""
    for command, CommandClass in COMMAND_MAP:
        if args[command]:
            CommandClass(args).action()
            return


def main():
    args = docopt(__doc__, version="ML Container Templates v0.0.1")
    try:
        run_command(args)
    except Exception as e:
        # ex: export MLT_DEBUG=1 will dump a traceback on fail
        if os.environ.get('MLT_DEBUG', '') != '':
            import traceback
            traceback.print_exc()
        else:
            print(e)
