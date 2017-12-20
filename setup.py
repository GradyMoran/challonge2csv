#!/usr/bin/env python

from setuptools import setup

setup(
    name='challonge2csv',
    version='0.0.1',
    description='A python module to create an excel file showing tournament placings.',
    license='',
    install_requires=['pychal==1.8.1', 'xlsxwriter', 'unicodecsv'],
    packages=['challonge2csv'],
    entry_points={
        'console_scripts': [
            'standings2csv = challonge2csv.__main__:standings2csv',
            'records2csv = challonge2csv.__main__:records2csv'
        ]
    }
)
