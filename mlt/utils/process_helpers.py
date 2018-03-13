import sys
from subprocess import check_output, CalledProcessError, Popen, PIPE, STDOUT


def run(command, cwd=None):
    try:
        output = check_output(command, cwd=cwd).decode("utf-8")
    except CalledProcessError as e:
        print(e.output)
        sys.exit(1)

    return output


def run_popen(command, shell=False):
    return Popen(command, stdout=PIPE, stderr=STDOUT, shell=shell)
