from mlt.commands.templates import Templates
from test_utils.io import catch_stdout


def test_template_list():
    templates = Templates({'template': True, 'list': True})
    with catch_stdout() as caught_output:
        templates.action()
        assert caught_output.getvalue() is not None
