#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='simulateur_ironcar',
    version='1.0.5.post2',
    packages=find_packages(exclude=["test_*"]),
    license='MIT license',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points = {
        'console_scripts': [
            'simulateur_ironcar = simulator.cli:cli',
        ],
    },
    include_package_data=True,
    package_data={
        'profil_generation_template': [
            'simulator/profil_generation_template/*',
            'simulator/profil_generation_template/grounds/*',
            'simulator/profil_generation_template/photos/*'
            'simulator/povray.pov'
        ],
    },
    install_requires=[
        'numpy',
        'matplotlib',
        'opencv-python',
        'Pillow',
        'click',
        'decorator'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pylint',
            'jupyter',
            'twine'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console"
    ]
)
