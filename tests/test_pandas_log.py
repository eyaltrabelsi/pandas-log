#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pandas_log` package."""

import numpy as np
import pandas as pd
import pytest
from numpy.random import randn


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


df = pd.DataFrame(randn(10, 2), columns=list('ab')) \
    .query('a > b')

df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
                   "toy": [np.nan, 'Batmobile', 'Bullwhip'],
                   "born": [pd.NaT, pd.Timestamp("1940-04-25"), pd.NaT]}) \
    .dropna()

df = pd.DataFrame(randn(10, 2), columns=list('ab')) \
    .dropna()

df = pd.DataFrame({'temp_c': [17.0, 25.0]},
                  index=['Portland', 'Berkeley']) \
    .assign(temp_f=lambda x: x.temp_c * 9 / 5 + 32)

df = pd.DataFrame({'temp_c': [17.0, 25.0]},
                  index=['Portland', 'Berkeley']) \
    .assign(temp_c=lambda x: x.temp_c * 9 / 5 + 32)

df = pd.DataFrame([('bird', 389.0),
                   ('bird', 24.0),
                   ('mammal', 80.5),
                   ('mammal', np.nan)],
                  index=['falcon', 'parrot', 'lion', 'monkey'],
                  columns=('class', 'max_speed'))
df.reset_index()

df = pd.DataFrame(randn(10, 2), columns=list('ab'))[:]
pass
