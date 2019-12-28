"""
uatu.py -
"""
from image_processing import ImageProcessing
from config_organizer import ConfigOrganizer
from acquisition import Acquisition
import random


class Uatu:
    """
    Uatu - he who watches
    """
    def __init__(self, config_file_path='../cfg/worldcams.cfg'):
        """
        __init__ - self
        """
        self.config_file = config_file_path
        self.cfg_organizer = ConfigOrganizer(config_file=self.config_file)
        self.cfg_organizer.read_config_data()


        self.acq_obj = Acquisition()

    def run(self):
        """
        run -
        """
        counter = 0
        for camera in self.cfg_organizer.find_cameras():
            self.acq_obj.retrieve(self.cfg_organizer.config_handler[camera]['url'], '/tmp/image.jpg')
            self.img_processing = ImageProcessing(yolo_path=
                                                  self.cfg_organizer.config_handler
                                                  ['system']['yolo_dir'])            
            self.img_processing.load_file('/tmp/image.jpg')
            self.img_processing.preprocess_image()
            self.img_processing.process_bounding_boxes()
            self.img_processing.output_adjusted_image('/tmp/what-{}.jpg'.format(counter))
            print(f'{camera} {self.img_processing.people_count}')
            counter += 1
            

    def debug_dump(self):
        print('Building camear information')
        for camera in self.cfg_organizer.find_cameras():
            print(f'{camera}')
            print('\t{}'.format(self.cfg_organizer.config_handler[camera]['url']))


if __name__ == "__main__":
    UATU_OBJ = Uatu()
    UATU_OBJ.run()
