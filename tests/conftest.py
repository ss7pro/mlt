from mock import MagicMock
import pytest
import os
import sys


# enable test_utils to be used in tests via `from test_utils... import ...
sys.path.append(os.path.join(os.path.dirname(__file__), 'test_utils'))
