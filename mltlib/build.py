import os
import time
import json
import uuid
import sys

from subprocess import Popen, PIPE, STDOUT
from watchdog.observers import Observer
from termcolor import colored

from . import progress_bar
from . import event_handler as eh


def build(args):
    if args['--watch']:
        event_handler = eh.EventHandler(do_build, args)
        observer = Observer()
        observer.schedule(event_handler, './', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    else:
        do_build(args)


def do_build(args):
    last_build_duration = None
    if os.path.isfile('.build.json'):
        status = json.load(open('.build.json'))
        last_build_duration = status['last_build_duration']

    started_build_time = time.time()

    config = json.load(open('mlt.json'))
    app_name = config['name']

    container_id = str(uuid.uuid4())
    container_name = app_name + ":" + container_id

    print("Starting build %s" % container_name)

    # Add bar
    build_process = Popen(["docker", "build", "-t", container_name, "."], stdout=PIPE, stderr=STDOUT)

    def build_is_done():
        return build_process.poll() is not None
    progress_bar.duration_progress('Building', last_build_duration, build_is_done)
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

    print("Built %s" % container_name)
