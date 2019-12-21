"""
All tests will be in @pytest markup format.

"""
import sys
import pytest
sys.path.append('../src')
from acquisition import Acquisition
import os

@pytest.mark.test_id(1)
def test_acquisition_creation():
    acquisition_obj = Acquisition()
    assert acquisition_obj is not None

@pytest.mark.test_id(2)
def test_acquisition_retrieval():
    acquisition_obj = Acquisition()
    acquisition_obj.retrieve("http://s1.twnmm.com/images/en_ca/icons/flags/all/16/ca.png","ca.png")
    assert os.path.exists("ca.png") == True

@pytest.mark.test_id(3)
def test_acquisition_bad_retrieval():
    acquisition_obj = Acquisition()
    try:
        acquisition_obj.retrieve("http://s1.twnmm.com/images/en_ca/icons/flags/all/16/ca.png","ca2.png")
        assert False
    except Exception as e:
        assert True
