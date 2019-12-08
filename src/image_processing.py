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
        self.img_height = 0
        self.img_width = 0
        self.raw_image = None
        self.modified_image = None
        self.processing_status = NONE
        """
        __init__
        """
        self.acquisition_time = time.time()
        self.prerequisite_settings(yolo_path)

    def prerequisite_settings(self, yolo_path=None):
        """
        load prerequisites
        """
        self.labels_path = os.path.sep.join([yolo_path, "coco.names"])
        self.labels = open(self.labels_path).read().strip().split("\n")

        # initialize the random seed
        np.random.seed(42)
        self.colours = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
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
                self.raw_image = cv2.imread(file_name)
                (self.img_height, self.img_width) = self.raw_image.shape[:2]
                self.processing_status = LOADED
            except IOError:
                print("File not accessible")
            finally:
                pass
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
            blob = cv2.dnn.blobFromImage(self.raw_image, 1 / 255.0,
                                         (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            start = time.time()
            layer_outputs = self.net.forward(self.layer_names)
            end = time.time()
            print("{} {}".format(start, end))
            boxes = []
            confidences = []
            class_ids = []
            # set to handle crap
            args = {}

            # loop over each of the layer outputs
            for output in layer_outputs:
                # loop over each of the detections
                for detection in output:
                    # extract the class ID and confidence (i.e., probability) of
                    # the current object detection
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > args["confidence"]:
                        # scale the bounding box coordinates back relative to the
                        # size of the image, keeping in mind that YOLO actually
                        # returns the center (x, y)-coordinates of the bounding
                        # box followed by the boxes' width and height
                        box = detection[0:4] * np.array([self.img_width,
                                                         self.img_height,
                                                         self.img_width,
                                                         self.img_height])
                        (center_x, center_y, width, height) = box.astype("int")

                        # use the center (x, y)-coordinates to derive the top and
                        # and left corner of the bounding box
                        x_corner = int(center_x - (width / 2))
                        y_corner = int(center_y - (height / 2))

                        # update our list of bounding box coordinates, confidences,
                        # and class IDs
                        boxes.append([x_corner, y_corner, int(width), int(height)])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
        return return_code

    def process_bounding_boxes(self):
        """
        get bounding box thingies

        boxes -
        confidences
        args - confidence
        args - threshold
        classIDs -
        x -
        y -
        h -
        w -

        self.colours
        """

    def output_adjusted_image(self, file_name=None):
        """
        draw bounding boxes and output to file
        """

if __name__=="__main__":
    x = ImageProcessing(yolo_path="../YOLO")
