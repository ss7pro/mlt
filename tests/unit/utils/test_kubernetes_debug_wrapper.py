#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

import pytest
from mock import patch

from mlt.utils import kubernetes_debug_wrapper
from test_utils.io import catch_stdout


@pytest.mark.parametrize("arg_value,enabled", [
    ("false", False),
    ("False", False),
    ("true", True),
    ("True", True)
])
@patch('mlt.utils.kubernetes_debug_wrapper.os.environ.get')
def test_debug_wrapper_enabled(mock_env_get, arg_value, enabled):
    """ Tests getting the proper debug_on_fail value based on test env vars """
    mock_env_get.return_value = arg_value
    assert kubernetes_debug_wrapper._get_debug_on_fail() == enabled


@patch('mlt.utils.kubernetes_debug_wrapper.sys.argv')
@patch('mlt.utils.kubernetes_debug_wrapper.open')
@patch('mlt.utils.kubernetes_debug_wrapper.compile')
def test_debug_wrapper_run_command(mock_compile, mock_open, mock_argv):
    """ Ensures we see the expected output when command is run """
    mock_argv.return_value = ["kubernetes_debug_wrapper.py", "main.py",
                              "--epochs", "10"]
    expected_output = "foo"
    mock_compile.return_value = "print('{}')".format(expected_output)

    with catch_stdout() as caught_output:
        kubernetes_debug_wrapper._run_command()
        output = caught_output.getvalue()

    assert expected_output in output


@patch('mlt.utils.kubernetes_debug_wrapper.traceback.print_exc')
@patch('mlt.utils.kubernetes_debug_wrapper.pdb.post_mortem')
@patch('mlt.utils.kubernetes_debug_wrapper.os.environ.get')
def test_start_debug(mock_env_get, mock_pdb, mock_traceback):
    """ Checks that when debug is initiated, a message is printing letting
    the user know how to attach to the failed pod. """
    test_hostname = "foo"
    mock_env_get.return_value = test_hostname

    with catch_stdout() as caught_output:
        with pytest.raises(SystemExit):
            kubernetes_debug_wrapper._start_debug()
        output = caught_output.getvalue()

    assert "kubectl attach -it {}".format(test_hostname) in output


@patch('mlt.utils.kubernetes_debug_wrapper._start_debug')
@patch('mlt.utils.kubernetes_debug_wrapper._run_command')
@patch('mlt.utils.kubernetes_debug_wrapper.os.environ.get')
def test_enabled_kubernetes_debug_wrapper(mock_env_get, mock_run_command,
                                          _mock_start_debug):
    """ Tests getting an error when the debug wrapper is enabled """
    # enabled debug_on_fail
    mock_env_get.return_value = "true"

    # simulate an error
    mock_run_command.side_effect = ValueError("foo")
    kubernetes_debug_wrapper.setup_debug_wrapper()

    # ensure that debug was started
    assert _mock_start_debug.called


@patch('mlt.utils.kubernetes_debug_wrapper._run_command')
@patch('mlt.utils.kubernetes_debug_wrapper.os.environ.get')
def test_disabled_kubernetes_debug_wrapper(mock_env_get, mock_run_command):
    """ Tests getting an error when the debug wrapper is disabled """
    # disabled debug_on_fail
    mock_env_get.return_value = "false"

    # simulate an error
    mock_run_command.side_effect = ValueError("foo")

    # we should get the error, since debug is disabled
    with pytest.raises(ValueError):
        kubernetes_debug_wrapper.setup_debug_wrapper()


@pytest.mark.parametrize("debug_on_fail", ["true", "false"])
@patch('mlt.utils.kubernetes_debug_wrapper._run_command')
@patch('mlt.utils.kubernetes_debug_wrapper.os.environ.get')
def test_debug_wrapper_keyboard_interrupt(mock_env_get, mock_run_command,
                                          debug_on_fail):
    """ Ensure that KeyboardInterrupt is raised, regardless of if debug is
    enabled or disabled """
    mock_env_get.return_value = debug_on_fail

    # simulate KeyboardInterrupt
    mock_run_command.side_effect = KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        kubernetes_debug_wrapper.setup_debug_wrapper()
