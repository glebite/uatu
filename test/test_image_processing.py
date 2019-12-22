"""
All tests will be in @pytest markup format.

"""
import sys
import pytest
import cv2
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
    ip_obj.preprocess_image()
    assert ip_obj.people_count == 6

@pytest.mark.test_id(4)
def test_image_processing_prerequisite_no_people():
    ip_obj = ImageProcessing(yolo_path="../YOLO")
    ip_obj.load_file("../static-images/no_people.jpg")
    ip_obj.preprocess_image()
    assert ip_obj.people_count == 0

@pytest.mark.test_id(5)
def test_image_processing_save_modified():
    ip_obj = ImageProcessing(yolo_path="../YOLO")
    ip_obj.load_file("../static-images/no_people.jpg")
    ip_obj.preprocess_image()
    ip_obj.process_bounding_boxes()
    ip_obj.output_adjusted_image("what.jpg")
    img = cv2.imread("what.jpg")
    assert img is not None
