#!/usr/bin/python
# coding=utf-8
import logging
import os
import shutil

import click
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@click.group()
@click.option('--verbose', '-v', is_flag=True)
def cli(verbose):
    configure_auto_logging(verbose)
    pass


def profil_generation_exists(cwd):
    return os.path.isfile(os.path.join(cwd, 'configuration.json'))


@click.command('init', help="initialiser un profile de génération de route")
def init():
    cwd = os.path.abspath(os.getcwd())
    configuration_target = os.path.abspath(cwd)
    profil_generation_template_path = os.path.join(ROOT_DIR, 'profil_generation_template')
    logger = logging.getLogger('simulateur_ironcar')

    if profil_generation_exists(cwd):
        logger.error('a profile for generation already exists in this directory')
        sys.exit(1)

    logger.debug({'operation': "create configuration profile", "configuration_target": configuration_target})
    ignores = ['.gitkeep']
    for root, _, files in os.walk(profil_generation_template_path):
        for file in files:
            dir_name = os.path.relpath(root, profil_generation_template_path)
            directory_target = os.path.join(configuration_target, dir_name)
            if not os.path.isdir(directory_target):
                logger.debug(
                    {'operation': "copy profile directory", "directory_target": directory_target})

                os.mkdir(directory_target)

            if file not in ignores:
                target = os.path.join(configuration_target, dir_name, file)
                logger.debug(
                    {'operation': "copy profile file", "target": target})

                shutil.copy(os.path.join(root, file), target)


@click.command('generate', help="générer les photographies à partir du profile de génération")
def generate():
    pass


def configure_auto_logging(force_debug=False):
    debug = force_debug or os.getenv('APP_DEBUG') == '1'
    level_info = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(format="%(asctime)s %(levelname)s - %(message)s [%(filename)s:%(lineno)s]", level=level_info)


cli.add_command(init)
cli.add_command(generate)

if __name__ == '__main__':
    cli()
