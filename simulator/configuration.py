#!/usr/bin/python
# coding=utf-8
import io
import json
import logging
import re

from colour import hex2rgb

SUPPORTED_VERSIONS = ["2019/02/23"]
MANDATORY_OPTIONS = [
    'version',
    'line_width_cm',
    'line_spread_cm',
    'dash_length_cm',
    'conversion_pixel_to_cm',
    'image_width',
    'image_height',
    'command_distance_cm',
    'origin_pool_start',
    'origin_pool_end',
    'origin_pool_step',
    'end_pool_top_start',
    'end_pool_top_end',
    'end_pool_top_step',
    'end_pool_right_start',
    'end_pool_right_end',
    'end_pool_right_step',
    'radius_pool_start',
    'radius_pool_end',
    'radius_pool_step',
    'images_curve'
]


def parse(configuration_path: str) -> dict:
    with io.open(configuration_path) as configuration_fp:
        conf = json.load(configuration_fp)

    check_integrity(conf, configuration_path)
    return _initialize(conf)


def check_integrity(configuration: dict, configuration_path: str = None):
    integrity = True
    message = 'missing mandatory options in {}'.format(configuration_path)
    for attribute in MANDATORY_OPTIONS:
        if attribute not in configuration:
            message += '\n  - {}'.format(attribute)
            integrity = False

    if not integrity:
        raise ConfigurationError(message)

def _initialize(configuration: dict, configuration_path: str = None) -> dict:
    logger = logging.getLogger('simulateur_ironcar')
    if "version" not in configuration:
        raise ConfigurationError('version attribute is required in {}'.format(configuration_path))

    if configuration["version"] not in SUPPORTED_VERSIONS:
        msg = 'version of configuration is not supported by this program {} - supported versions of configuration : {}'
        raise ConfigurationError(msg.format(configuration["version"], SUPPORTED_VERSIONS))

    dataset_pattern = re.compile(r'(?:^[^_=]*$)')
    if "dataset_id" in configuration:
        if not dataset_pattern.fullmatch(configuration["dataset_id"]):
            raise ConfigurationError(
                'dataset_id attribute does not allow _ and = - {}'.format(configuration["dataset_id"]))
    else:
        configuration['dataset_id'] = "dataset"

    if 'road_median_line_color' not in configuration:
        default_road_median_line_color = '#66ec04'
        configuration['road_median_line_color'] = hex2rgb255(default_road_median_line_color)
        logger.warning('road_median_line_color is missing from %s. default value : %s',
                       configuration_path, default_road_median_line_color)
    else:
        road_median_line_color = configuration['road_median_line_color']
        try:
            configuration['road_median_line_color'] = hex2rgb255(road_median_line_color)
        except ValueError:
            raise ConfigurationError(
                'road_median_line_color should be an hexadecimal web value as #ffffff, instead : {}'.format(
                    road_median_line_color))

    return configuration


def hex2rgb255(color):
    """
    cv2 requires rgb color encoded on 255 values instead of rgb encoded
    as a float value between 0 and 1

    :see https://docs.opencv.org/3.1.0/dc/da5/tutorial_py_drawing_functions.html
    :param color:
    :return:
    """
    red, green, blue = hex2rgb(color)
    rgb255_color = (int(red * 255), int(green * 255), int(blue * 255))
    return rgb255_color


class ConfigurationError(Exception):
    pass
