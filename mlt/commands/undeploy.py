from mlt.commands.base import Command
from mlt.utils import config_helpers, process_helpers


class UndeployCommand(Command):
    def __init__(self, args):
        super(UndeployCommand, self).__init__(args)
        self.config = config_helpers.load_config()

    def action(self):
        """deletes current kubernetes namespace"""
        namespace = self.config['namespace']
        process_helpers.run(
            ["kubectl", "--namespace", namespace, "delete", "-f", "k8s"])
