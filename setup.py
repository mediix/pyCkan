"""
Python package to fetch datasets via CKAN API.

See:
https://github.com
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyCkan',
    version='0.1',
    description='A simple ckan dataset fetch project',
    long_description=long_description,
    url='https://github.com/pypa/sampleproject',
    author='Mehdi Nazari',
    author_email='mnazari@gvhomes.com',
    license='MIT',
    keywords='Dataset Collection',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: GranvilleHomes Administration Office',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'mysql-python',
        'sqlAlchemy',
        'requests'
    ],
    data_files=[
        ('Schema', ['src/main/data/ckan_database_schema.mwb']),
        ('Model', ['src/main/data/model.pdf']),
    ],
    entry_points={
        'console_scripts': [
            'ckan-fetch' = '',
            'ckan-update' = '',
            'ckan-verify' = '',
        ],
    },
)
