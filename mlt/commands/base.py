class Command(object):
    def __init__(self, args):
        self.args = args

    def action(self):
        raise NotImplementedError()
