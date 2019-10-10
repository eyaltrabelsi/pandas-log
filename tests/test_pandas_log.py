#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pandas_log` package."""

import pandas as pd

from pandas_log import *


def test_pipeline():
    with enable():
        #     auto_enable()
        df = pd.read_csv("../examples/pokemon.csv")
        df2 = df.copy()
        (
            df.query("legendary==0")
            .query("type_1=='fire' or type_2=='fire'")
            .drop("legendary", axis=1)
            .nsmallest(1, "total")
            .assign(type_1=lambda x: x.type_1)
            .reset_index(drop=True)
        )
        # auto_disable()
    df.head()

    df2.query("legendary==1").query("type_1=='fire' or type_2=='fire'").drop(
        "legendary", axis=1
    ).nsmallest(1, "total").assign(type_1=lambda x: x.type_1).reset_index(
        drop=True
    )

    pass
    # df1 = pd.DataFrame(
    #         {"lkey": ["foo", "bar", "baz", "foo"], "value": [1, 2, 3, 5]}
    #     )
    # df2 = pd.DataFrame(
    #         {"rkey": ["foo", "bar", "baz", "foo"], "value": [5, 6, 7, 8]}
    #     )
    # df1.merge(df2, left_on="lkey", right_on="rkey")

    # df = pd.DataFrame(
    #     {
    #         "key": ["K0", "K1", "K2", "K3", "K4", "K5"],
    #         "A": ["A0", "A1", "A2", "A3", "A4", "A5"],
    #     }
    # )
    # other = pd.DataFrame(
    #     {"key": ["K0", "K1", "K2"], "B": ["B0", "B1", "B2"]}
    # )
    # df.join(other, lsuffix="_caller", rsuffix="_other")


test_pipeline()
