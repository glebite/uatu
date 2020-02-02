"""
convertor.py 

Converts the old .csv file data to an SQLite database.
"""
import logging
from operator import itemgetter
import sys
from os import path


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FH = logging.FileHandler('conversion.log')
FORMATTER = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
FH.setFormatter(FORMATTER)
FH.setLevel(logging.DEBUG)
LOGGER.addHandler(FH)


class Convertor:
    """
    Convertor
    """
    def __init__(self, input_name=None, output_name=None):
        """
        __init__ method - defines any class values needed
        """
        LOGGER.info("Instantiating class")
        self.input_name = input_name
        self.output_name = output_name
        
        # people do count - this is why we are doing this 
        self.headers = ['camera_name', 'timestamp', 'people_count']

    def KPI(self):
        """
        KPI
        - an early attempt to bring KPI values into my home code
        """
        LOGGER.info(f"KPI: class_size {sys.getsizeof(self)}")

    def record_iterator(self):
        with open(self.input_name,'r') as input_file:
            single_line = input_file.readline()
            yield {k:v for (k,v) in zip(self.headers, single_line.split(',')[0:3])}

    def convert(self):
        for line in self.record_iterator():
            print(line)
            break

        
def main():
    try:
        input_name, output_name = itemgetter(1,2)(sys.argv)
    except IndexError:
        LOGGER.error("Index error - sys.argv needs 2 values for input and output name respectively.")
        sys.exit(-1)

    if not path.exists(input_name):
        LOGGER.error(f"{input_name} does not exist.")
        sys.exit(-2)
        
    uatu_conv = Convertor(input_name, output_name)
    uatu_conv.KPI()
    uatu_conv.convert()



if __name__ == "__main__":
    main()

    

    
