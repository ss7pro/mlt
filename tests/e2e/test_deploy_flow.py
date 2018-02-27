from contextlib import contextmanager
import json
import shutil
import subprocess
import tempfile
import os


@contextmanager
def create_work_dir():
    workdir = tempfile.mkdtemp()
    try:
        yield workdir
    finally:
        # still need to remove dir when done
        # https://docs.python.org/2/library/tempfile.html#tempfile.mkdtemp
        shutil.rmtree(workdir)


# don't want to combine everything but in order to test each part you need
# whole flow built on itself
# TODO: figure out a better way maybe?
def test_flow():
    with create_work_dir() as workdir:
        project_dir = os.path.join(workdir, 'foobar')
        mlt_json = os.path.join(project_dir, 'mlt.json')
        build_json = os.path.join(project_dir, '.build.json')
        deploy_json = os.path.join(project_dir, '.push.json')

        # mlt init
        p = subprocess.Popen(
            ['mlt', 'init', '--registry=localhost:5001', 'foobar'],
            cwd=workdir)
        assert p.wait() == 0
        assert os.path.isfile(mlt_json)
        with open(mlt_json) as f:
            assert json.loads(f.read()) == {
                'namespace': 'foobar',
                'name': 'foobar',
                'registry': 'localhost:5000'
            }

        # mlt build
        p = subprocess.Popen(['mlt', 'build'], cwd=project_dir)
        assert p.wait() == 0
        assert os.path.isfile(build_json)
        with open(build_json) as f:
            build_data = json.loads(f.read())
            assert 'last_container' in build_data and \
                'last_build_duration' in build_data

        # mlt deploy
        p = subprocess.Popen(['mlt', 'deploy'], cwd=project_dir)
        out, err = p.communicate()
        assert p.wait() == 0
        assert os.path.isfile(deploy_json)
        with open(deploy_json) as f:
            deploy_data = json.loads(f.read())
            assert 'last_push_duration' in deploy_data and \
                'last_remote_container' in deploy_data

        # mlt undeploy
        p = subprocess.Popen(['mlt', 'undeploy'], cwd=project_dir)
        assert p.wait() == 0
