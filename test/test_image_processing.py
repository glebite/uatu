"""
All tests will be in @pytest markup format.

"""
import sys
import pytest
sys.path.append('../src')
from image_processing import ImageProcessing

@pytest.mark.test_id(1)
def test_image_processing_creation():
    ip_obj = ImageProcessing(yolo_path="../YOLO")
    assert ip_obj is not None
    
@pytest.mark.test_id(3)
def test_image_processing_prerequisite_does_not_crash():
    ip_obj = ImageProcessing(yolo_path="../YOLO")
    ip_obj.load_file("../static-images/4_or_more_people_clinic.jpeg")
    mt = ip_obj.preprocess_image()
    assert mt.people_count == 6

@pytest.mark.test_id(4)
def test_image_processing_prerequisite_no_people():
    ip_obj = ImageProcessing(yolo_path="../YOLO")
    ip_obj.load_file("../static-images/no_people.jpg")
    mt = ip_obj.preprocess_image()
    assert mt.people_count == 0
