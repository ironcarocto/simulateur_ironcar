#!/usr/bin/python
# coding=utf-8
import os

import click

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


@click.group()
def cli():
    pass


@click.command('init', help="initialiser un profile de génération de route")
def init():
    pass


@click.command('generate', help="générer les photographies à partir du profile de génération")
def generate():
    pass


cli.add_command(init)
cli.add_command(generate)

if __name__ == '__main__':
    cli()
