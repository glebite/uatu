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
    # pylint: disable=too-many-instance-attributes

    def __init__(self, yolo_path=None):
        # image could be consolidated into one dictionary
        # image = {'height': 0, 'width': 0, 'raw_image': None, 'modified_image': None}
        self.img_height = 0
        self.img_width = 0
        self.raw_image = None
        self.modified_image = None
        self.processing_status = NONE
        self.boxes = list()
        self.confidences = None
        self.confidence = None
        self.threshold = None
        self.class_ids = list()
        # box could be consolidated into a dictionary:
        # box = {'x': 0, 'y': 0, 'height': 0, 'width': 0}
        self.x_pos = None
        self.y_pos = None
        self.box_height = None
        self.box_width = None
        self.people_count = 0
        self.args = None
        """
        __init__
        """
        self.acquisition_time = time.time()
        self.prerequisite_settings(yolo_path)

    def prerequisite_settings(self, yolo_path=None):
        """
        load prerequisites
        """
        # TODO: error checking
        self.labels_path = os.path.sep.join([yolo_path, "coco.names"])
        self.labels = open(self.labels_path).read().strip().split("\n")

        # initialize the random seed
        np.random.seed(42)
        self.colours = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")
        self.weights_path = os.path.sep.join([yolo_path, "yolov3.weights"])
        self.config_path = os.path.sep.join([yolo_path, "yolov3.cfg"])
        self.net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def load_file(self, file_name=None):
        """
        load_file - loads the file
        """
        if os.path.isfile(file_name):
            try:
                self.raw_image = cv2.imread(file_name)
                (self.img_height, self.img_width) = self.raw_image.shape[:2]
                self.processing_status = LOADED
            except IOError:
                raise IOError
            except AttributeError:
                raise AttributeError
            finally:
                pass
        else:
            raise IOError

    def preprocess_image(self):
        """
        preprocessing routine - people
        """
        # pylint: disable=too-many-instance-attributes

        if self.processing_status is not LOADED:
            print("Error...  not loaded - cannot process")
        else:
            blob = cv2.dnn.blobFromImage(self.raw_image, 1 / 255.0,
                                         (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            layer_outputs = self.net.forward(self.layer_names)
            self.boxes = []
            self.confidences = []
            class_ids = []
            self.args = {'confidence': 0.9, 'threshold': 0.9}

            for output in layer_outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > self.args["confidence"]:
                        self.people_count += 1
                        box = detection[0:4] * np.array([self.img_width,
                                                         self.img_height,
                                                         self.img_width,
                                                         self.img_height])
                        (center_x, center_y, width, height) = box.astype("int")
                        x_corner = int(center_x - (width / 2))
                        y_corner = int(center_y - (height / 2))
                        self.boxes.append([x_corner, y_corner, int(width), int(height)])
                        self.confidences.append(float(confidence))
                        self.class_ids.append(class_id)

    def process_bounding_boxes(self):
        """
        get bounding box thingies

        """
        idxs = cv2.dnn.NMSBoxes(self.boxes,
                                self.confidences,
                                self.args["confidence"],
                                self.args["threshold"])

        self.modified_image = cv2.copyMakeBorder(self.raw_image,0,0,0,0,cv2.BORDER_REPLICATE)        
        count = 0
        # ensure at least one detection exists
        if len(idxs):
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                (self.x_pos, self.y_pos) = (self.boxes[i][0], self.boxes[i][1])
                (self.box_width, self.box_height) = (self.boxes[i][2], self.boxes[i][3])

                # draw a bounding box rectangle and label on the image
                color = [int(c) for c in self.colours[self.class_ids[i]]]
                cv2.rectangle(self.modified_image, (self.x_pos, self.y_pos),
                              (self.x_pos + self.box_width, self.y_pos + self.box_height),
                              color, 2)
                text = "{}: {:.4f}".format(self.labels[self.class_ids[i]], self.confidences[i])
                if "person" in text:
                    count += 1
                    cv2.putText(self.modified_image, text, (self.x_pos, self.y_pos - 5)
                                , cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    def output_adjusted_image(self, file_name=None):
        """
        draw bounding boxes and output to file
        """
        # TODO: should probably do some error handling here...
        try:
            cv2.imwrite(file_name, self.modified_image)
        except IOError:
            raise IOError
        
