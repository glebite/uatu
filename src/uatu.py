"""
uatu.py -
"""
from image_processing import ImageProcessing
from config_organizer import ConfigOrganizer
from acquisition import Acquisition


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
        self.img_processing = ImageProcessing(yolo_path=
                                              self.cfg_organizer.config_handler
                                              ['system']['yolo_dir'])

        self.acq_obj = Acquisition()

    def run(self):
        """
        run -
        """


if __name__ == "__main__":
    UATU_OBJ = Uatu()
