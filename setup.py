#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["humanize>=0.5.0", "pandas>=0.25.1", "pandas_flavor>=0.1.2"]

setup(
    name='pandas-log',
    version='0.1.7',
    description="pandas-log provides feedback about basic pandas operations. It provides simple wrapper functions for "
                "the most common functions, such as apply, map, query and more.",
    author="Eyal Trabelsi",
    author_email='eyaltrabelsi@gmail.com',
    url='https://github.com/eyaltrabelsi/pandas-log',
    packages=find_packages(include=['pandas_log', 'pandas_log.*']),
    install_requires=requirements,
    python_requires=">=3.4",
    license="MIT license",
    long_description="pandas-log provides feedback about basic pandas operations. It provides simple wrapper functions "
                     "for the most common functions, such as apply, map, query and more.",
    long_description_content_type="text/x-rst",
    extras_require={'development': ['bump2version==0.5.11', 'tox==3.14.0', 'Sphinx==3.0.4', 'twine==3.1.1', 'pytest==5.1.3', 'pandas==0.25.1', 'pandas_flavor==0.1.2', 'humanize==0.5.0', 'nbval==0.9.5', 'ipykernel==5.2.0']},

)
