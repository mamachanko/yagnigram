#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'binaryornot==0.3.0',
    'blessings==1.6',
    'click==3.3',
    'docopt==0.6.2',
    'falcon==0.2',
    'httplib2==0.9',
    'Jinja2==2.7.3',
    'MarkupSafe==0.23',
    'mock==1.0.1',
    'Pillow==2.7.0',
    'python-instagram==1.3.0',
    'python-mimeparse==0.1.4',
    'PyYAML==3.11',
    'requests==2.5.3',
    'simplejson==3.6.5',
    'six==1.9.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='yagnigram',
    version='0.1.0',
    description="The Instagram command line client you ain't going to need.",
    long_description=readme + '\n\n' + history,
    author="mamachanko",
    author_email='max@rootswiseyouths.com',
    url='https://github.com/mamachanko/yagnigram',
    packages=[
        'yagnigram',
    ],
    package_dir={'yagnigram':
                 'yagnigram'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='yagnigram',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
