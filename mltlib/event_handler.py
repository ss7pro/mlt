import time
import os
from threading import Timer
from subprocess import call

class EventHandler:
    def __init__(self, callback, args):
        self.args = args
        self.last_changed = time.time()
        self.dirty = False
        self.timer = None
        self.callback = callback

    def dispatch(self, event):
        if event.src_path == "./.git" or event.src_path == "./":
            return

        is_ignored = call(["git", "check-ignore", event.src_path], stdout=open(os.devnull, 'wb')) == 0
        if is_ignored:
            return

        if self.timer:
            self.timer.cancel()

        print("event.src_path %s" % event.src_path)

        def timer_triggered():
            self.callback(self.args)

        self.timer = Timer(3, timer_triggered)
        self.timer.start()