"""
ImageProcessing
"""
import time
import os
import numpy as np
import cv2

NONE = 0
PREPROCESSED = 1
PROCESSED = 2


class ImageProcessing:
    """
    ImageProcessing class
    """
    def __init__(self):
        """
        __init__
        """
        self.raw_image = None
        self.modified_image = None
        self.processing_status = NONE
        self.acquisition_time = time.time()

    def load_file(self, file_name=None):
        """
        load_file - loads the file
        """
        if os.path.isfile(file_name):
            print("exists")
            try:
                file_handler = open(file_name)
                self.raw_image = file_handler.read()
            except IOError:
                print("File not accessible")
            finally:
                file_handler.close()
        else:
            print("not exist")

    def preprocess_image(self):
        """
        preprocessing routine - people
        """
        pass

    def process_bounding_boxes(self):
        """
        get bounding box thingies
        """
        pass

    def output_adjusted_image(self, file_name=None):
        """
        draw bounding boxes and output to file
        """
        pass
