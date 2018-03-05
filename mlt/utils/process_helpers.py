import sys
from subprocess import check_output, CalledProcessError, Popen, PIPE, STDOUT


def run(command, cwd=None):
    try:
        output = check_output(command, cwd=cwd).decode("utf-8")
    except CalledProcessError as e:
        print(e.output)
        sys.exit(1)

    return output


def run_popen(command_array):
    return Popen(command_array, stdout=PIPE, stderr=STDOUT)


def run_popen_unsecure(command_string):
    return Popen(command_string, stdout=PIPE, stderr=STDOUT, shell=True)
