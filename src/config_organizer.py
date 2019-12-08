"""
config_organizer - more than just a parser but builds what is needed
"""
import os
import configparser

class config_organizer:
    """
    config_organizer - configuration file class and other data
    """
    def __init__(self, config_file=None):
        """
        initialize file and configuration data
        """
        if os.path.isfile(config_file):
            self.config_file = config_file            
        else:
            raise IOError

    def read_config_data(self):
        # something
        pass
    
if __name__=="__main__":
    pass
