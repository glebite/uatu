"""

"""
import sys
import pytest
sys.path.append('../src')
from config_organizer import config_organizer

@pytest.mark.test_id(1)
def test_config_organizer_creation():
    config_organizer_obj = config_organizer(config_file='./test.cfg')
    assert config_organizer_obj is not None


@pytest.mark.test_id(2)
def test_config_organizer_test_config():
    config_organizer_obj = config_organizer(config_file="./test.cfg")
    assert config_organizer_obj.read_config_data()['test']['test_value'] == '13'
