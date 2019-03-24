#!/usr/bin/python
# coding=utf-8
import io
import json

SUPPORTED_VERSIONS = ["2019/02/23"]


def parse(configuration_path):
    with io.open(configuration_path) as configuration_fp:
        conf = json.load(configuration_fp)

    if "version" not in conf:
        raise ConfigurationError('version attribute is required in {}'.format(configuration_path))

    if conf["version"] not in SUPPORTED_VERSIONS:
        raise ConfigurationError(
            'version of configuration is not supported by this program {} - supported versions of configuration : {}'.format(
                conf["version"],
                SUPPORTED_VERSIONS))

    return conf


class ConfigurationError(Exception):

    def __init__(self, message):
        super().__init__(message)
