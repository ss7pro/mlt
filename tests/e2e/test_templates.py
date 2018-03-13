from subprocess import check_output
from test_utils import project


def test_templates():
    output = check_output(['mlt', 'templates', 'list',
                           '--template-repo={}'.format(project.basedir())]
                          ).decode("utf-8")
    assert len(output.split('\n')) == 5
