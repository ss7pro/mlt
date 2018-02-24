import time
import json
import uuid
import sys

from watchdog.observers import Observer
from termcolor import colored

from mlt.commands import NeedsInitCommand
from mlt.event_handler import EventHandler
from mlt.utils import progress_bar
from mlt.utils.process_helpers import run_popen


class Build(NeedsInitCommand):
    def action(self):
        """creates docker images
           if `--watch` is passed, continually will build on change
        """
        self._watch_and_build() if self.args['--watch'] else self._build()

    def _build(self):
        last_build_duration = self._fetch_action_arg(
            'build', 'last_build_duration')

        started_build_time = time.time()

        container_name = "{}:{}".format(self.config['name'], uuid.uuid4())
        print("Starting build {}".format(container_name))

        # Add bar
        build_process = run_popen(
            ["docker", "build", "-t", container_name, "."])

        progress_bar.duration_progress(
            'Building', last_build_duration,
            lambda: build_process.poll() is not None)
        if build_process.poll() != 0:
            print(colored(build_process.communicate()[0], 'red'))
            sys.exit(1)

        built_time = time.time()

        # Write last container to file
        with open('.build.json', 'w') as f:
            f.write(json.dumps({
                "last_container": container_name,
                "last_build_duration": built_time - started_build_time
            }))

        print("Built {}".format(container_name))

    def _watch_and_build(self):
        event_handler = EventHandler(self._build)
        observer = Observer()
        # TODO: what dir was this?
        observer.schedule(event_handler, './', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()
        observer.join()
