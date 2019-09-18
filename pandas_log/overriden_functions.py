# -*- coding: utf-8 -*-

"""Main module."""

import warnings
from contextlib import suppress
from functools import wraps
from inspect import signature
from types import FunctionType

import pandas as pd
import pandas_flavor as pf

from pandas_log.utils import *

__all__ = ["enable", "disable"]


def _get_pandas_func(func):
    return getattr(pd.DataFrame, f"original_{func.__name__}")


def _get_patch_log_func(func):
    res = None
    with suppress(AttributeError):
        res = getattr(
            __import__("pandas_log.patched_functions").patched_functions,
            f"_log_{func.__name__}",
        )
    return res


def _restore_pandas_func_copy(func):
    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, func.replace("original_", ""), original_method)


def _keep_pandas_func_copy(func):
    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, f"original_{func}", original_method)


def _create_overide_pandas_func(func):
    # todo
    func_code = compile(
        f"@overide_dataframe_method\ndef {func}(df, *arg, **kwarg):\n\tpass",
        "<generated-ast>",
        "exec",
    )
    foo_func = FunctionType(func_code, globals(), func)
    overide_dataframe_method(foo_func)


def _get_str_signature(fn, args):
    relevant_args = list(
        zip(args, signature(_get_pandas_func(fn)).parameters)
    )[1:]
    return "({})".format(
        ",".join(f'{name}="{value}"' for value, name in relevant_args)
    )


def _logs_fn_stats(fn, t, args, **fn_params):
    sig = _get_str_signature(fn, args)
    print(f"{fn.__name__}{sig}:")
    print(f"\t* Step Took {t.interval_humanize}")
    log_method = _get_patch_log_func(fn)
    if log_method:
        logs = log_method(**fn_params)
        print(logs)


def overide_dataframe_method(fn):
    @pf.register_dataframe_method
    @wraps(fn)
    def wrapped(*args, **kwargs):
        with Timer() as t:
            output_df = _get_pandas_func(fn)(*args, **kwargs)

        df = args[0]
        _logs_fn_stats(**locals())
        return output_df

    return wrapped


def disable():
    for func in dir(pd.DataFrame):
        if func.startswith("original_"):
            _restore_pandas_func_copy(func)


def enable():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for func in dir(pd.DataFrame):
            if not func.startswith("_"):
                _keep_pandas_func_copy(func)
                # _create_overide_pandas_func(func)

        @overide_dataframe_method
        def query(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def dropna(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def drop(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def assign(df, **kwargs):
            pass

        @overide_dataframe_method
        def reset_index(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def sort_index(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def sort_values(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def head(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def tail(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def sample(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def fillna(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def merge(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def join(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def nlargest(df, *args, **kwargs):
            pass

        @overide_dataframe_method
        def nsmallest(df, *args, **kwargs):
            pass


if __name__ == "__main__":
    enable()
    disable()
    enable()
    from numpy.random import randn

    df = pd.DataFrame(randn(10, 2), columns=list("ab")).query("a > b")
