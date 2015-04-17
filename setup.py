#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'arrow==0.5.4',
    'blessings==1.6',
    'docopt==0.6.2',
    'falcon==0.2',
    'Pillow==2.7.0',
    'python-instagram==1.3.0',
    'requests==2.5.3',
    'six==1.9.0',
]

setup(
    name='yagnigram',
    version='0.1.0',
    description="The Instagram command line client you ain't going to need.",
    long_description=readme,
    author="mamachanko",
    author_email='max@rootswiseyouths.com',
    url='https://github.com/mamachanko/yagnigram',
    packages=find_packages(),
    package_dir={'yagnigram': 'yagnigram'},
    install_requires=requirements,
    entry_points={'console_scripts': ['yagnigram = yagnigram.cli:cli'],
    }
)
