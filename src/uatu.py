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
import pandas as pd
import concurrent.futures

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
        self.current_max_count()
        LOGGER.info("Completed initialization.")

    def __repr__(self):
        return f"<Uatu - path: {self.config_file}>"

    def current_max_count(self):
        """
        current_max_count - returns the current maximum count for the cameras
        """
        namelist = ['name', 'timestamp', 'count']

        # TODO: nuke the fixed path later
        df = pd.read_csv(self.cfg_organizer.config_handler['system']['csv_location'], index_col=False, names=namelist)

        df2 = df.fillna(0)
        camera_names = df['name'].unique()
        df2.sort_values(by=['name', 'count'], inplace=True)
        series = df2.groupby('name')['count'].max()
        self.stored_values = series.to_dict()

    def acquire_images(self):
        """
        acquire_images
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            camera_futures = {executor.submit(self.acq_obj.retrieve,self.cfg_organizer.config_handler[camera]['url'], '/tmp/{}-image.jpg'.format(camera)): camera for camera in self.cfg_organizer.find_cameras()}
            for future in concurrent.futures.as_completed(camera_futures):
                camera = camera_futures[future]
                try:
                    data = future.result()
                    LOGGER.info(f'data? {data}')
                except Exception as e:
                    LOGGER.error(f'exception {e}')
                else:
                    LOGGER.info('got it')

    def process_images(self):
        """
        process_images
        """
        pass

    def run(self):
        """
        run - executor method
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
            processed_image = "/tmp/{}-{}-{}.jpg".format(camera, time.time(), self.img_processing.people_count)
            self.img_processing.output_adjusted_image('/tmp/what-{}.jpg'.format(counter))
            print("{},{},{},{}".format(camera, time.time(), self.img_processing.people_count, processed_image))
            if  int(self.img_processing.people_count) > int(self.stored_values[camera]):
                LOGGER.info("New Max value acheived! Stored: {} New: {}".format(self.stored_values[camera],
                                                                                self.img_processing.people_count))
                LOGGER.info("Camera image: {}".format(processed_image))
                self.img_processing.output_adjusted_image(processed_image)
            LOGGER.info("camera: {} people: {}".format(camera,self.img_processing.people_count))
        
    def debug_dump(self):
        LOGGER.debug('Building camera information')
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.debug(f'{camera}')
            LOGGER.debug('\t{}'.format(self.cfg_organizer.config_handler[camera]['url']))


if __name__ == "__main__":
    UATU_OBJ = Uatu(sys.argv[1])
    UATU_OBJ.run()
