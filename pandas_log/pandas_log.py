# -*- coding: utf-8 -*-

"""Main module."""

import warnings
from contextlib import contextmanager
from functools import wraps

import pandas as pd

import pandas_flavor as pf
from pandas_log import settings
from pandas_log.aop_utils import (
    calc_step_number,
    get_pandas_func,
    keep_pandas_func_copy,
    restore_pandas_func_copy,
)
from pandas_log.pandas_execution_stats import StepStats, get_execution_stats

__all__ = ["auto_enable", "auto_disable", "enable"]


ALREADY_ENABLED = False


def auto_disable():
    """ Restore original pandas method without the additional log functionality (statistics)
        Note: we keep the original methods using original_ prefix.
        :return: None
    """
    global ALREADY_ENABLED
    if not ALREADY_ENABLED:
        return

    for func in dir(pd.DataFrame):
        if func.startswith(settings.ORIGINAL_METHOD_PREFIX):
            restore_pandas_func_copy(func)
    ALREADY_ENABLED = False


@contextmanager
def enable(verbose=False, silent=False, full_signature=True):
    """ Adds the additional logging functionality (statistics) to pandas methods only for the scope of this
        context manager.

        :param verbose: Whether some inner functions should be recorded as well.
                        For example: when a dataframe being copied
        :param silent: Whether additional the statistics get printed
        :param full_signature: adding additional information to function signature
        :return: None
    """

    auto_enable(verbose, silent, full_signature)
    yield
    auto_disable()


def auto_enable(verbose=False, silent=False, full_signature=True):
    """ Adds the additional logging functionality (statistics) to pandas methods.

        :param verbose: Whether some inner functions should be recorded as well.
                        For example: when a dataframe being copied
        :param silent: Whether additional the statistics get printed
        :param full_signature: adding additional information to function signature
        :return: None
    """
    global ALREADY_ENABLED
    if ALREADY_ENABLED:
        return

    settings.PANDAS_METHODS_TO_OVERIDE.extend(
        settings.PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
    )

    # Suppressing warning of the fact we override pandas functions.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for func in dir(pd.DataFrame):
            if func in settings.PANDAS_METHODS_TO_OVERIDE:
                keep_pandas_func_copy(func)
                create_overide_pandas_func(
                    func, verbose, silent, full_signature
                )
    ALREADY_ENABLED = True


def create_overide_pandas_func(func, verbose, silent, full_signature):
    """ Create overridden pandas method dynamically with
        additional logging using DataFrameLogger

        Note: if we extracting _overide_dataframe_method outside we need to implement decorator like here
              https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator

        :param func: pandas method name to be overridden
        :param silent: Whether additional the statistics get printed
        :param full_signature: adding additional information to function signature
        :return: the same function with additional logging capabilities
    """

    def _run_method_and_calc_stats(
        fn, fn_args, fn_kwargs, input_df, full_signature, silent, verbose
    ):

        output_df, execution_stats = get_execution_stats(
            fn, input_df, fn_args, fn_kwargs
        )

        step_stats = StepStats(
            execution_stats,
            fn,
            fn_args,
            fn_kwargs,
            full_signature,
            input_df,
            output_df,
        )

        step_stats.persist_execution_stats()
        step_stats.log_stats_if_needed(silent, verbose)
        return output_df

    def _overide_dataframe_method(fn):
        @pf.register_dataframe_method
        @wraps(fn)
        def wrapped(*args, **fn_kwargs):

            input_df, fn_args = args[0], args[1:]
            output_df = _run_method_and_calc_stats(
                fn,
                fn_args,
                fn_kwargs,
                input_df,
                full_signature,
                silent,
                verbose,
            )
            return output_df

        return wrapped

    return exec(
        f"@_overide_dataframe_method\ndef {func}(df, *args, **kwargs): pass"
    )


if __name__ == "__main__":
    pass
