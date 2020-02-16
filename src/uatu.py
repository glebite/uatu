from image_processing import ImageProcessing
from acquisition import Acquisition
from config_organizer import ConfigOrganizer

import requests
import time
import sys
import logging
import pandas as pd
import threading
from multiprocessing import Lock
from queue import Queue


LOGGER = logging.getLogger('uatu')
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler('uatu.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOGGER.addHandler(FH)

NUM_WORKER_THREADS = 4

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
        self.img_processing = ImageProcessing(yolo_path=self.cfg_organizer.config_handler['system']['yolo_dir'])  

    def __repr__(self):
        return "string"

    def current_max_count(self):
        """
        current_max_count - returns the current maximum count for the cameras
        """
        namelist = ['name', 'timestamp', 'count']

        df = pd.read_csv(self.cfg_organizer.config_handler['system']['csv_location'], index_col=False, names=namelist)

        df2 = df.fillna(0)
        camera_names = df['name'].unique()
        df2.sort_values(by=['name', 'count'], inplace=True)
        series = df2.groupby('name')['count'].max()
        self.stored_values = series.to_dict()

    def producer_images(self, pqueue, cqueue, lock):
        while True:
            if not pqueue.empty():
                camera_name = pqueue.get()
                image_name = '/tmp/{}-image.jpg'.format(camera_name)
                try:
                    self.acq_obj.retrieve(self.cfg_organizer.config_handler[camera_name]['url'], image_name)
                    with lock:
                        LOGGER.debug(f'retrieved image: {camera_name}')
                    cqueue.put((camera_name, image_name))
                except Exception as e:
                    with lock:
                        LOGGER.debug(f'exception: {e}')
        # pqueue.task_done()
        
    def consumer_process_image(self, cqueue, lock):
        counter = 1
        while True:
            if cqueue.empty():
                continue
            camera_name, image_name = cqueue.get()
            with lock:
                LOGGER.debug(f'processing camera: {camera_name}')
            try:
                with lock:
                    self.img_processing.load_file(f'/tmp/{camera_name}-image.jpg')
            except IOError:
                with lock:
                    LOGGER.debug(f'yup - io error - skipping {camera_name}')
                return
            with lock:
                self.img_processing.preprocess_image()
            with lock:
                self.img_processing.process_bounding_boxes()
            processed_image = "/tmp/{}-{}-{}.jpg".format(camera_name, time.time(), self.img_processing.people_count)
            with lock:
                self.img_processing.output_adjusted_image('/tmp/what-{}.jpg'.format(counter))
            with lock:
                print("{},{},{},{}".format(camera_name, time.time(), self.img_processing.people_count, processed_image))
            if  int(self.img_processing.people_count) > int(self.stored_values[camera_name]):
                self.img_processing.output_adjusted_image(processed_image)

    def doit(self):
        self.current_max_count()
        
        pqueue = Queue(maxsize = 0)
        cqueue = Queue(maxsize = 0)
        
        lock = Lock()

        for i in range(NUM_WORKER_THREADS):
            pworker = threading.Thread(target=self.producer_images, args=(pqueue, cqueue, lock))
            pworker.daemon = True
            pworker.start()
            LOGGER.debug('initiated pworkers')
            cworker = threading.Thread(target=self.consumer_process_image, args=(cqueue, lock))
            cworker.daemon = True
            cworker.start()
            LOGGER.debug('initiated workers')
        
        cameras = self.cfg_organizer.find_cameras()
        for camera_name in cameras:
            LOGGER.debug(f'Loading {camera_name} into pqueue')
            pqueue.put(camera_name)
            
        cworker.join()

    def debug_dump(self):
        LOGGER.debug('Building camera information')
        for camera in self.cfg_organizer.find_cameras():
            LOGGER.debug(f'{camera}')
            LOGGER.debug('\t{}'.format(self.cfg_organizer.config_handler[camera]['url']))


if __name__ == "__main__":
    UATU_OBJ = Uatu(sys.argv[1])
    UATU_OBJ.doit()
