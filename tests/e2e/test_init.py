import tempfile
import subprocess
import os

def test_init():
    workdir = tempfile.mkdtemp()
    p = subprocess.Popen(['mlt', 'init', '--registry=registry:5000', 'foobar'], cwd=workdir)
    assert p.wait() == 0
    project_dir = workdir + '/foobar'
    assert os.path.isfile(project_dir + '/.studio.json')

    p = subprocess.Popen(['mlt', 'build'], cwd=project_dir)
    assert p.wait() == 0