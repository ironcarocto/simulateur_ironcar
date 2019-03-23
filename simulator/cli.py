#!/usr/bin/python
# coding=utf-8
import json
import logging
import os
import shutil

import click
import sys

import io

from simulator.pictures_generation import generate_profile_for_cadran

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@click.group()
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    configure_auto_logging(verbose)
    pass


@click.command('init', help="initialiser un profile de génération de route")
def init():
    cwd = os.path.abspath(os.getcwd())
    profile_target = os.path.abspath(cwd)
    profil_generation_template_path = os.path.join(ROOT_DIR, 'profil_generation_template')
    logger = logging.getLogger('simulateur_ironcar')

    if profil_generation_exists(cwd):
        logger.error('a profile for generation already exists in this directory')
        sys.exit(1)

    logger.debug({'operation': "create configuration profile", "configuration_target": profile_target})
    ignores = ['.gitkeep']
    for root, _, files in os.walk(profil_generation_template_path):
        for file in files:
            dir_name = os.path.relpath(root, profil_generation_template_path)
            directory_target = os.path.join(profile_target, dir_name)
            if not os.path.isdir(directory_target):
                logger.debug(
                    {'operation': "copy profile directory", "directory_target": directory_target})

                os.mkdir(directory_target)

            if file not in ignores:
                target = os.path.join(profile_target, dir_name, file)
                logger.debug(
                    {'operation': "copy profile file", "target": target})

                shutil.copy(os.path.join(root, file), target)


def profil_generation_exists(cwd):
    return os.path.isfile(os.path.join(cwd, 'configuration.json'))


@click.command('generate', help="générer les photographies à partir du profile de génération")
def generate():
    cwd = os.path.abspath(os.getcwd())
    profile_directory = os.path.abspath(cwd)
    logger = logging.getLogger('simulateur_ironcar')
    if not profil_generation_exists(profile_directory):
        logger.error('a profile for road generation does not exists - start a profile with simulateur_ironcar init')
        sys.exit(1)

    with io.open(os.path.join(profile_directory, 'configuration.json')) as configuration_fp:
        configuration = json.load(configuration_fp)

    for i in range(0, 5):
        generate_profile_for_cadran(cadran_id=i,
                                    configuration=configuration,
                                    ground_path=os.path.join(profile_directory, 'grounds'),
                                    photos_path= os.path.join(profile_directory, 'photos')
        )


def configure_auto_logging(force_debug=False):
    debug = force_debug or os.getenv('APP_DEBUG') == '1'
    level_info = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)s - %(message)s [%(filename)s:%(lineno)s]", level=level_info)


cli.add_command(init)
cli.add_command(generate)

if __name__ == '__main__':
    cli()
