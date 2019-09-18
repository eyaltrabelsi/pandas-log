#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pandas_log` package."""

import numpy as np
import pandas as pd

from pandas_log import enable


def test_pipeline():
    df = (
        pd.DataFrame(
            {
                "name": ["Alfred", "Batman", "Catwoman"],
                "toy": [np.nan, "Batmobile", "Bullwhip"],
                "born": [pd.NaT, pd.Timestamp("1940-04-25"), pd.NaT],
            }
        )
        .dropna()
        .assign(toy=lambda x: x.toy.map(str.lower))
        .assign(lower_name=lambda x: x.name.map(str.lower))
        .query("name != 'Batman'")
        .reset_index()
    )


#  \
enable()
test_pipeline()
