from mock import patch
from mock_open import MockOpen
import os
import pytest
import shutil
import uuid

from mlt.commands.init import InitCommand
from test_utils.io import catch_stdout


def test_init_dir_exists():
    new_dir = str(uuid.uuid4())
    os.mkdir(new_dir)
    init_dict = {'init': True, '--template': 'hello-world', '<name>': new_dir}
    try:
        with catch_stdout() as caught_output:
            with pytest.raises(SystemExit) as bad_init:
                InitCommand(init_dict).action()
                assert caught_output.getvalue() == \
                    "Directory '{}' already exists: delete ".format(
                        new_dir) + "before trying to initialize new " + \
                    "application"
                assert bad_init.value.code == 1
    finally:
        os.rmdir(new_dir)


@patch('mlt.commands.init.shutil')
@patch('mlt.commands.init.process_helpers')
@patch('mlt.commands.init.open')
def test_init(open_mock, proc_helpers, shutil_mock):
    open_mock = MockOpen()
    new_dir = str(uuid.uuid4())
    init_dict = {
        'init': True,
        '--template': 'hello-world',
        '<name>': new_dir,
        '--registry': None
    }
    init = InitCommand(init_dict)
    with patch('mlt.commands.init.check_output') as check_output_mock:
        check_output_mock.return_value.decode.return_value = 'tacos'
        init.action()
    assert init.app_name == new_dir


@patch('mlt.commands.init.shutil')
@patch('mlt.commands.init.process_helpers')
@patch('mlt.commands.init.open')
def test_init(open_mock, proc_helpers, shutil_mock):
    open_mock = MockOpen()
    new_dir = str(uuid.uuid4())
    init_dict = {
        'init': True,
        '--template': 'hello-world',
        '<name>': new_dir,
        '--registry': True
    }
    init = InitCommand(init_dict)
    init.action()
    assert init.app_name == new_dir
