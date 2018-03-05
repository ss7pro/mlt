from mock import patch
import pytest

from mlt.utils.build_helpers import verify_build


@patch('mlt.utils.build_helpers.BuildCommand')
def test_needs_build_command_bad_build(BuildClass):
    verify_build({})
    assert BuildClass.return_value.action.called
