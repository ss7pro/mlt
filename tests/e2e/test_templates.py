from subprocess import check_output

def test_templates():
    output = check_output(['mlt', 'templates', 'list']).decode("utf-8")
    assert len(output.split('\n')) == 5