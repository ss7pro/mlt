import os


# Returns the absolute path to the MLT project directory.
def basedir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    relative_path = os.path.join(script_dir, "..", "..")
    return os.path.abspath(relative_path)

