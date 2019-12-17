"""

"""
import sys
import pytest
sys.path.append('../src')
from config_organizer import ConfigOrganizer

@pytest.mark.test_id(1)
def test_ConfigOrganizer_creation():
    co_obj = ConfigOrganizer(config_file='./test.cfg')
    assert co_obj is not None

@pytest.mark.test_id(2)
def test_ConfigOrganizer_test_config():
    co_obj = ConfigOrganizer(config_file="./test.cfg")
    assert co_obj.read_config_data()['test']['test_value'] == '13'

@pytest.mark.test_id(3)
def test_config_count_entries():
    co_obj = ConfigOrganizer(config_file="./test.cfg")
    config_info = co_obj.read_config_data()
    assert len(config_info) == 4

@pytest.mark.test_id(4)
def test_config_wildcard_camers():
    co_obj = ConfigOrganizer(config_file="./test.cfg")
    co_obj.read_config_data()
    assert len(co_obj.find_cameras()) == 2

@pytest.mark.test_id(5)
def test_get_camera_1_city():
    co_obj = ConfigOrganizer(config_file="./test.cfg")
    co_obj.read_config_data()
    assert co_obj.config_handler['camera_1']['city'] == "Fars"   
