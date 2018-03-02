import pytest

from mlt.utils.config_helpers import load_config

from test_utils.io import catch_stdout


def test_needs_init_command_bad_init():
    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit) as bad_init:
            load_config()
            assert caught_output.getvalue() == "This command requires you " + \
                "to be in an `mlt init` built directory"
            assert bad_init.value.code == 1
