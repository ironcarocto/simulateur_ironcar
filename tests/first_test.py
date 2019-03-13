import json
import os
import glob
from definitions import CONFIG_PATH
from simulator.pictures_generation import right_direction

TEST_CONTEXT_DIR_PATH = '/Users/constant.bridon/Documents/IronCar/simulateur_octo/tests/photos/'
TEST_OUTPUT_DIR_PATH = TEST_CONTEXT_DIR_PATH + 'output/'


def setup_function(*args):
    images = glob.glob(TEST_OUTPUT_DIR_PATH+'*.png')
    [os.remove(x) for x in images]


def test_right_direction_should_save_twice_as_many_images_as_configuration():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 3

    # Where
    right_direction(configuration, execution_dir_path=TEST_CONTEXT_DIR_PATH, output_dir=TEST_OUTPUT_DIR_PATH)

    # Then
    image_number = count_png(TEST_OUTPUT_DIR_PATH)
    assert image_number == 2 * configuration['images_curve']


def count_png(photos_path_test):
    images_produced_by_povray = [x for x in os.listdir(photos_path_test) if x.endswith('.png')]
    image_number_init = len(images_produced_by_povray)
    return image_number_init
