#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='simulator_ironcar',
    version='1.0.2',
    packages=find_packages(exclude=["*_tests"]),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': [
            'simulateur_ironcar = simulator.cli:cli',
        ],
    },
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python',
        'Pillow',
        'click'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pylint',
            'jupyter'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console"
    ]
)
