"""
uatu.py -
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
        LOGGER.info("initializing UATU")
        self.config_file = config_file_path
        self.cfg_organizer = ConfigOrganizer(config_file=self.config_file)
        self.cfg_organizer.read_config_data()
        self.acq_obj = Acquisition()

    def run(self):
        """
        run -
        """
        LOGGER.info("running...")
        csv_output = ""
        counter = 1
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.info("Working on camera: {}".format(camera))
            counter += 1
            try:
                self.acq_obj.retrieve(self.cfg_organizer.config_handler[camera]['url'], '/tmp/image.jpg')
            except requests.exceptions.Timeout  as e:
                # stuff
                LOGGER.info("Failure in camera retrieval for {}".format(camera))
                csv_output += "{},{},NaN,".format(camera, time.time())                
                continue
            self.img_processing = ImageProcessing(yolo_path=
                                                  self.cfg_organizer.config_handler
                                                  ['system']['yolo_dir'])            
            self.img_processing.load_file('/tmp/image.jpg')
            self.img_processing.preprocess_image()
            self.img_processing.process_bounding_boxes()
            self.img_processing.output_adjusted_image('/tmp/what-{}.jpg'.format(counter))
            csv_output += "{},{},{},".format(camera, time.time(), self.img_processing.people_count)
            LOGGER.info("camera: {} people: {}".format(camera,self.img_processing.people_count))
        print(csv_output)
        
    def debug_dump(self):
        LOGGER.debug('Building camera information')
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.debug(f'{camera}')
            LOGGER.debug('\t{}'.format(self.cfg_organizer.config_handler[camera]['url']))


if __name__ == "__main__":
    UATU_OBJ = Uatu(sys.argv[1])
    UATU_OBJ.run()
