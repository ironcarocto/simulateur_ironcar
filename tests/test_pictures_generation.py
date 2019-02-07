import json
import os

from definitions import CONFIG_PATH
from simulator.pictures_generation import straight, points_selection
from utils import Point


def test_first_to_fail():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 2
    PHOTOS_PATH = '/Users/constant.bridon/Documents/IronCar/simulateur_octo/photos/'
    images_produced_by_povray = [x for x in os.listdir(PHOTOS_PATH) if x.endswith('.png')]
    image_number_init = len(images_produced_by_povray)

    # Where
    right_direction(configuration)
    images_produced_by_povray = [x for x in os.listdir(PHOTOS_PATH) if x.endswith('.png')]
    image_number_end = len(images_produced_by_povray)

    # Then
    image_number = image_number_end - image_number_init
    assert image_number == 2 * configuration['images_curve']


def test_():
    # Given

    expected = (Point(500, 500), Point(600, 600))

    # When
    result = points_selection((500, 500), (600, 600))

    # Then
    assert result == expected


def test_():
    # Given
    CONFIG_PATH = '../configuration.json'
    configuration = json.load(open(CONFIG_PATH))

    straight(configuration)

    # Then
    assert result == expected
