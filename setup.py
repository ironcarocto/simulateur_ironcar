#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='simulator_ironcar',
    version='1.0.1',
    packages=find_packages(exclude=["*_tests"]),
    license='',
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python',
        'Pillow'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pylint',
            'jupyter'
        ]
    }
)
