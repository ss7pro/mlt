import os
import shutil
from subprocess import check_output
from . import process_helpers


def init(args):
    template_directory = "/".join([os.path.dirname(__file__), "..", "templates", args["--template"]])
    app_name = args["<name>"]
    try:
        shutil.copytree(template_directory, app_name)

        raw_project_bytes = check_output(["gcloud", "config", "list", "--format", "value(core.project)"])
        project = raw_project_bytes.decode("utf-8").strip()

        with open(app_name + '/.studio.json', 'w') as f:
            f.write('''
{
  "name": "%s",
  "namespace": "%s",
  "gceProject": "%s"
}
''' % (app_name, app_name, project))

        # Initialize new git repo in the project dir and commit initial state.
        process_helpers.run(["git", "init", app_name])
        process_helpers.run(["git", "add", "."], cwd=app_name)
        print(process_helpers.run(["git", "commit", "-m", "Initial commit."], cwd=app_name))

    except OSError as exc:
        if exc.errno == 17:
            print("Directory '%s' already exists: delete before trying to initialize new application" % app_name)
        else:
            print(exc)
