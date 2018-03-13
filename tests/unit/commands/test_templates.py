from mlt.commands.templates import TemplatesCommand
from test_utils.io import catch_stdout
from test_utils import project


def test_template_list():
    args = {
        'template': 'test',
        'list': True,
        '--template-repo': project.basedir()
    }
    templates = TemplatesCommand(args)
    with catch_stdout() as caught_output:
        templates.action()
        assert caught_output.getvalue() is not None
