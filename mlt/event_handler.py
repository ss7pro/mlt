import time
import os
from threading import Timer
from subprocess import call


class EventHandler(object):
    def __init__(self, callback, args):
        self.args = args
        self.last_changed = time.time()
        self.dirty = False
        self.timer = None
        self.callback = callback

    def dispatch(self, event):
        if event.src_path in ("./.git", "./"):
            return

        is_ignored = call(["git", "check-ignore", event.src_path],
                          stdout=open(os.devnull, 'wb')) == 0
        if is_ignored:
            return

        if self.timer:
            self.timer.cancel()

        print("event.src_path {}".format(event.src_path))

        self.timer = Timer(3, lambda: self.callback(self.args))
        self.timer.start()
