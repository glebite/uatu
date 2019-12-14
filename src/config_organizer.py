"""
config_organizer - more than just a parser but builds what is needed
"""
import os
import configparser


class ConfigOrganizer:
    """
    ConfigOrganizer - configuration file class and other data
    """
    def __init__(self, config_file=None):
        """
        initialize file and configuration data
        """
        if os.path.isfile(config_file):
            self.config_file = config_file
            self.config_handler = configparser.ConfigParser()
        else:
            raise IOError

    def read_config_data(self):
        """ read_config_data """
        self.config_handler.read(self.config_file)
        return self.config_handler

    def find_cameras(self):
        """ find_cameras """
        cameras = [match_string for match_string in self.config_handler
                   if "camera_" in match_string]
        return cameras
