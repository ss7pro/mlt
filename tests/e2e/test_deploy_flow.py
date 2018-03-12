from contextlib import contextmanager
import json
import os
import getpass
import shutil
import subprocess
import tempfile
import uuid

from mlt.utils.process_helpers import run, run_popen_unsecure


@contextmanager
def create_work_dir():
    workdir = tempfile.mkdtemp()
    try:
        yield workdir
    finally:
        # even on error we still need to remove dir when done
        # https://docs.python.org/2/library/tempfile.html#tempfile.mkdtemp
        shutil.rmtree(workdir)


# don't want to combine everything but in order to test each part you need
# whole flow built on itself
# TODO: figure out a better way maybe?
def test_flow():
    # just in case tests fail during development, want a clean namespace always
    app_name = str(uuid.uuid4())[:10]
    namespace = getpass.getuser() + app_name
    with create_work_dir() as workdir:
        project_dir = os.path.join(workdir, app_name)
        mlt_json = os.path.join(project_dir, 'mlt.json')
        build_json = os.path.join(project_dir, '.build.json')
        deploy_json = os.path.join(project_dir, '.push.json')

        # mlt init
        p = subprocess.Popen(
            ['mlt', 'init', '--registry=localhost:5000',
             '--namespace={}'.format(namespace), app_name], cwd=workdir)
        assert p.wait() == 0
        assert os.path.isfile(mlt_json)
        with open(mlt_json) as f:
            assert json.loads(f.read()) == {
                'namespace': namespace,
                'name': app_id,
                'registry': 'localhost:5000'
            }
        # verify we created a git repo with our project init
        assert "On branch master" in run(
            "git --git-dir={}/.git --work-tree={} status".format(
                project_dir, project_dir).split())

        # mlt build
        p = subprocess.Popen(['mlt', 'build'], cwd=project_dir)
        assert p.wait() == 0
        assert os.path.isfile(build_json)
        with open(build_json) as f:
            build_data = json.loads(f.read())
            assert 'last_container' in build_data and \
                'last_build_duration' in build_data
            # verify that we created a docker image
            assert run_popen_unsecure(
                "docker image inspect {}".format(build_data['last_container'])
            ).wait() == 0

        # mlt deploy
        p = subprocess.Popen(['mlt', 'deploy'], cwd=project_dir)
        out, err = p.communicate()
        assert p.wait() == 0
        assert os.path.isfile(deploy_json)
        with open(deploy_json) as f:
            deploy_data = json.loads(f.read())
            assert 'last_push_duration' in deploy_data and \
                'last_remote_container' in deploy_data
        # verify that the docker image has been pushed to our local registry
        # need to decode because in python3 this output is in bytes
        assert 'true' in run_popen_unsecure(
            "curl --noproxy \"*\"  registry:5000/v2/_catalog | "
            "jq .repositories | jq 'contains([\"{}\"])'".format(namespace)
        ).stdout.read().decode("utf-8")
        # verify that our job did indeed get deployed to k8s
        assert run_popen_unsecure(
            "kubectl get jobs --namespace={}".format(namespace)).wait() == 0

        # mlt undeploy
        p = subprocess.Popen(['mlt', 'undeploy'], cwd=project_dir)
        assert p.wait() == 0
        # verify no more deployment job
        assert run_popen_unsecure(
            "kubectl get jobs --namespace={}".format(namespace)
        ).wait() == 0
