#!/usr/bin/env python

from setuptools import setup

setup(
    name='challonge2csv',
    version='0.0.1',
    description='A tool to fetch ',
    license='',
    install_requires=['requests', 'bs4'],
    packages=['challonge2csv'],
    entry_points={
        'console_scripts': [
            'standings2csv = challonge2csv.__main__:standings2csv',
            'records2csv = challonge2csv.__main__:player_records2csv'
        ]
    }
)
