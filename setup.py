#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3',]

setup(
    name='pandas-log',
    version='0.1.5',
    description="pandas-log provides feedback about basic pandas operations. It provides simple wrapper functions for the most common functions, such as apply, map, query and more.",
    author="Eyal Trabelsi",
    author_email='eyaltrabelsi@gmail.com',
    url='https://github.com/eyaltrabelsi/pandas-log',
    packages=find_packages(include=['pandas_log', 'pandas_log.*']),
    install_requires=requirements,
    python_requires=">=3.4",
    license="MIT license",
    long_description="pandas-log provides feedback about basic pandas operations. It provides simple wrapper functions for the most common functions, such as apply, map, query and more.",
    long_description_content_type="text/x-rst",
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements
)
