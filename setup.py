"""
Python package to fetch London Datastore datasets via CKAN API.

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
    name='pyCKAN',
    version='0.1',
    description='Python Package to Fetch London Datastore Datasets via CKAN API',
    long_description=long_description,
    url='https://github.com/mediix/pyCkan.git',
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
            'ckan = src.main.python.cmd:main',
            'ckan_fetch = src.main.python.cmd:ckan_fetch',
            'ckan_update = src.main.python.cmd:ckan_update',
            'ckan_verify = src.main.python.cmd:ckan_verify',
        ],
    },
)
