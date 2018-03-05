import os

from mlt.commands.build import BuildCommand


def verify_build(args):
    """runs a full build if no build json file"""
    if not os.path.isfile('.build.json'):
        BuildCommand(args).action()
