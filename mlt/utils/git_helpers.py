from contextlib import contextmanager
from mlt.utils import process_helpers
import shutil
import tempfile


@contextmanager
def clone_repo(repo):
    destination = tempfile.mkdtemp()
    process_helpers.run(["git", "clone", repo, destination])
    try:
        yield destination
    finally:
        shutil.rmtree(destination)
