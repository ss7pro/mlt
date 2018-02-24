from contextlib import contextmanager
try:
    # python 2
    from cStringIO import StringIO
except ImportError:
    # python 3
    # only supports unicode so can't be used in python 2 for sys.stdout
    # because (from `print` documentation)
    # "All non-keyword arguments are converted to strings like str() does"
    from io import StringIO
import sys
from mlt.commands.templates import Templates


@contextmanager
def catch_stdout():
    _stdout = sys.stdout
    sys.stdout = caught_output = StringIO()
    try:
        yield caught_output
    finally:
        sys.stdout = _stdout
        caught_output.close()


def test_template_list():
    templates = Templates({'template': True, 'list': True})
    with catch_stdout() as caught_output:
        templates.action()
        assert caught_output.getvalue() is not None
