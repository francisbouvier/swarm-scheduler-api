#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

requires = [
    'tornado',
    'docker-py',
]

setup(
    name='swarm-scheduler-api',
    version='0.1.0',  # 3 numbers notation major.minor.bugfix_or_security
    description='Swarm scheduler API example',
    author='Francis Bouvier ',
    author_email='francis.bouvier@gmail.com',
    license='New BSD License',
    platforms='Any',
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False,
    include_package_data=True,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'swarm-scheduler-api = swarm_scheduler_api.server:main',
        ]
    }
)
