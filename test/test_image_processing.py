"""
All tests will be in @pytest markup format.

"""
import sys
import pytest
sys.path.append('../src')
from image_processing import ImageProcessing

@pytest.mark.test_id(1)
def test_image_processing_creation():
    ip_obj = ImageProcessing()
    assert ip_obj is not None
