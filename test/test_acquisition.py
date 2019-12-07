"""
All tests will be in @pytest markup format.

"""
import sys
import pytest
sys.path.append('../src')
from acquisition import Acquisition

@pytest.mark.test_id(1)
def test_acquisition_creation():
    acquisition_obj = Acquisition()
    assert acquisition_obj is not None
