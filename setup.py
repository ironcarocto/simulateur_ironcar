#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='simulator',
    version='1.0.0.dev0',
    packages=find_packages(exclude=["*_tests"]),
    license='',
    install_requires=[],
    extras_require={
        'dev': [
            'pytest',
            'jupyter',
            'Pillow',
            'numpy',
            'matplotlib',
            'pytest',
            'opencv-python'
        ]
    }
)
