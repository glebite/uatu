"""
uatu.py - he who watches
"""
from image_processing import ImageProcessing
from config_organizer import ConfigOrganizer
from acquisition import Acquisition
import random
import requests
import time
import sys
import logging

LOGGER = logging.getLogger('uatu')
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler('uatu.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOGGER.addHandler(FH)

class Uatu:
    """
    Uatu - he who watches
    """
    def __init__(self, config_file_path):
        """
        __init__ - self
        """
        LOGGER.info("Initializing UATU.")
        self.config_file = config_file_path
        self.cfg_organizer = ConfigOrganizer(config_file=self.config_file)
        self.cfg_organizer.read_config_data()
        self.acq_obj = Acquisition()
        LOGGER.info("Completed initialization.")

    def run(self):
        """
        run -
        """
        LOGGER.info("Running.")
        csv_output = ""
        counter = 1
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.info("Working on camera: {}.".format(camera))
            counter += 1
            try:
                LOGGER.info("Retrieving image and saving to /tmp/image.jpg .")
                self.acq_obj.retrieve(self.cfg_organizer.config_handler[camera]['url'], '/tmp/image.jpg')
            except requests.exceptions.Timeout  as e:
                # stuff
                LOGGER.info("Failure in camera retrieval for {} - csv output has NaN now.".format(camera))
                print("{},{},NaN,".format(camera, time.time()))
                continue
            LOGGER.info("Performing image processing.")
            self.img_processing = ImageProcessing(yolo_path=
                                                  self.cfg_organizer.config_handler
                                                  ['system']['yolo_dir'])            
            self.img_processing.load_file('/tmp/image.jpg')
            self.img_processing.preprocess_image()
            self.img_processing.process_bounding_boxes()
            self.img_processing.output_adjusted_image('/tmp/what-{}.jpg'.format(counter))
            print("{},{},{},".format(camera, time.time(), self.img_processing.people_count))
            LOGGER.info("camera: {} people: {}".format(camera,self.img_processing.people_count))
        
    def debug_dump(self):
        LOGGER.debug('Building camera information')
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.debug(f'{camera}')
            LOGGER.debug('\t{}'.format(self.cfg_organizer.config_handler[camera]['url']))


if __name__ == "__main__":
    UATU_OBJ = Uatu(sys.argv[1])
    UATU_OBJ.run()
