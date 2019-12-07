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
LOADED = 4


class ImageProcessing:
    """
    ImageProcessing class
    """
    def __init__(self, yolo_path=None):
        """
        __init__
        """
        self.raw_image = None
        self.modified_image = None
        self.processing_status = NONE
        self.acquisition_time = time.time()
        self.prerequisite_settings(yolo_path)

    def prerequisite_settings(self, yolo_path=None):
        """
        load prerequisites
        """
        self.labels_path = os.path.sep.join([yolo_path, "coco.names"])
        self.labels = open(self.labels.path).read().strip().split("\n")

        # initialize the random seed
        np.random.seed(time.time())
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.weights_path = os.path.sep.join([yolo_path, "yolov3.weights"])
        self.config_path = os.path.sep.join([yolo_path, "yolov3.cfg"])
        print("[INFO] loading YOLO from disk...")
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

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
        return_code = True
        if self.processing_status is not LOADED:
            print("Error...")
            return_code = False
        else:
            print("Success?")

        return return_code

    def process_bounding_boxes(self):
        """
        get bounding box thingies
        """

    def output_adjusted_image(self, file_name=None):
        """
        draw bounding boxes and output to file
        """
