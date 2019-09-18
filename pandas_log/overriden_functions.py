# -*- coding: utf-8 -*-

"""Main module."""

import warnings
from functools import wraps

import pandas as pd
import pandas_flavor as pf

from pandas_log import patched_functions
from pandas_log.utils import *

__all__ = ["enable", "disable"]


def overide_dataframe_method(fn):
    @pf.register_dataframe_method
    @wraps(fn)
    def wrapped(*args, **kwargs):
        with Timer() as t:
            res = fn(*args, **kwargs)
        print(f"Took {t.interval}\n")
        return res

    return wrapped


def disable():
    overriden_pandas_funcs = [
        func for func in dir(pd.DataFrame) if func.startswith("original_")
    ]
    for overriden_pandas_func in overriden_pandas_funcs:
        original_method = getattr(pd.DataFrame, overriden_pandas_func)
        setattr(
            pd.DataFrame,
            overriden_pandas_func.replace("original_", ""),
            original_method,
        )


def enable():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        overriden_pandas_funcs = [func for func in dir(pd.DataFrame) if not func.startswith("_")]
        for overriden_pandas_func in overriden_pandas_funcs:
            original_method = getattr(pd.DataFrame, overriden_pandas_func)
            setattr(pd.DataFrame, f"original_{overriden_pandas_func}", original_method)
        #
        #     patched_method = pf.register_dataframe_method(_patch_log_method(original_method))
        #     setattr(pd.DataFrame, overriden_pandas_func, patched_method)

        @overide_dataframe_method
        def query(input_df, expr, inplace=False, **kwargs):
            output_df = input_df.original_query(expr, inplace, **kwargs)
            patched_functions._log_query(input_df, output_df, expr)
            return output_df

        @overide_dataframe_method
        def dropna(
            input_df,
            axis=0,
            how="any",
            thresh=None,
            subset=None,
            inplace=False,
        ):
            output_df = input_df.original_dropna(
                axis, how, thresh, subset, inplace
            )
            patched_functions._log_dropna(input_df, output_df)
            return output_df

        @overide_dataframe_method
        def drop(
            input_df,
            labels=None,
            axis=0,
            index=None,
            columns=None,
            level=None,
            inplace=False,
            errors="raise",
        ):
            output_df = input_df.original_drop(
                labels, axis, index, columns, level, inplace, errors
            )
            patched_functions._log_dropna(input_df, output_df)
            return output_df

        @overide_dataframe_method
        def assign(input_df, **kwargs):
            output_df = input_df.original_assign(**kwargs)
            patched_functions._log_assign(input_df, assign_cols=kwargs.keys())
            return output_df

        @overide_dataframe_method
        def reset_index(
            input_df,
            level=None,
            drop=False,
            inplace=False,
            col_level=0,
            col_fill="",
        ):
            output_df = input_df.original_reset_index(
                level, drop, inplace, col_level, col_fill
            )
            patched_functions._log_reset_index()
            return output_df

        @overide_dataframe_method
        def sort_index(
            input_df,
            axis=0,
            level=None,
            ascending=True,
            inplace=False,
            kind="quicksort",
            na_position="last",
            sort_remaining=True,
            by=None,
        ):
            output_df = input_df.original_sort_index(
                axis,
                level,
                ascending,
                inplace,
                kind,
                na_position,
                sort_remaining,
                by,
            )
            patched_functions._log_sort_index(ascending)
            return output_df

        @overide_dataframe_method
        def sort_values(
            input_df,
            by,
            axis=0,
            ascending=True,
            inplace=False,
            kind="quicksort",
            na_position="last",
        ):
            output_df = input_df.original_sort_values(
                by, axis, ascending, inplace, kind, na_position
            )
            patched_functions._log_sort_values(by, ascending)
            return output_df

        @overide_dataframe_method
        def head(input_df, n=5):
            output_df = input_df.original_head(n)
            patched_functions._log_head(n)
            return output_df

        @overide_dataframe_method
        def tail(input_df, n=5):
            output_df = input_df.original_tail(n)
            patched_functions._log_tail(n)
            return output_df

        @overide_dataframe_method
        def sample(
            input_df,
            n=None,
            frac=None,
            replace=False,
            weights=None,
            random_state=None,
            axis=None,
        ):
            output_df = input_df.original_sample(
                n, frac, replace, weights, random_state, axis
            )
            patched_functions._log_sample(output_df)
            return output_df

        @overide_dataframe_method
        def fillna(
            input_df,
            value=None,
            method=None,
            axis=None,
            inplace=False,
            limit=None,
            downcast=None,
            **kwargs,
        ):
            output_df = input_df.original_fillna(
                value, method, axis, inplace, limit, downcast, **kwargs
            )
            patched_functions._log_fillna(input_df, output_df)
            return output_df

        @overide_dataframe_method
        def merge(
            input_df,
            other_input_df,
            how="inner",
            on=None,
            left_on=None,
            right_on=None,
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("_x", "_y"),
            copy=True,
            indicator=False,
            validate=None,
        ):
            output_df = input_df.original_merge(
                other_input_df,
                how,
                on,
                left_on,
                right_on,
                left_index,
                right_index,
                sort,
                suffixes,
                copy,
                indicator,
                validate,
            )
            patched_functions._log_merge(
                input_df, other_input_df, output_df, how
            )
            return output_df

        @overide_dataframe_method
        def join(
            input_df,
            other_input_df,
            on=None,
            how="left",
            lsuffix="",
            rsuffix="",
            sort=False,
        ):
            output_df = input_df.original_join(
                other_input_df, on, how, lsuffix, rsuffix, sort
            )
            patched_functions._log_join(
                input_df, other_input_df, output_df, how
            )
            return output_df

        @overide_dataframe_method
        def nlargest(input_df, n, columns, keep="first"):
            output_df = input_df.original_nlargest(n, columns, keep)
            patched_functions._log_nlargest(n, columns)
            return output_df

        @overide_dataframe_method
        def nsmallest(input_df, n, columns, keep="first"):
            output_df = input_df.original_nsmallest(n, columns, keep)
            patched_functions._log_nsmallest(n, columns)
            return output_df


if __name__ == "__main__":
    enable()
    disable()
    enable()
    from numpy.random import randn

    df = pd.DataFrame(randn(10, 2), columns=list("ab")).query("a > b")
