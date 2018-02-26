import os
import sys
import shutil
from subprocess import check_output
from mlt.utils import process_helpers


def init(args):
    template_directory = "/".join([os.path.dirname(__file__),
                                   "..", "..", "templates",
                                   args["--template"]])
    app_name = args["<name>"]

    print(args)
    is_gke = args["--registry"] is None

    try:
        shutil.copytree(template_directory, app_name)

        if is_gke:
            raw_project_bytes = check_output(
                ["gcloud", "config", "list", "--format",
                 "value(core.project)"])
            project = raw_project_bytes.decode("utf-8").strip()

            with open(app_name + '/mlt.json', 'w') as f:
                f.write('''
{
"name": "%s",
"namespace": "%s",
"gceProject": "%s"
}
    ''' % (app_name, app_name, project))

        else:
            with open(app_name + '/mlt.json', 'w') as f:
                f.write('''
{
"name": "%s",
"namespace": "%s",
"registry": "%s"
}
    ''' % (app_name, app_name, args["--registry"]))

        # Initialize new git repo in the project dir and commit initial state.
        process_helpers.run(["git", "init", app_name])
        process_helpers.run(["git", "add", "."], cwd=app_name)
        print(process_helpers.run(
            ["git", "commit", "-m", "Initial commit."], cwd=app_name))

    except OSError as exc:
        if exc.errno == 17:
            print(
                "Directory '%s' already exists: delete before trying to "
                "initialize new application" % app_name)
        else:
            print(exc)

        sys.exit(1)
