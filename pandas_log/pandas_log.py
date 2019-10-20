# -*- coding: utf-8 -*-

"""Main module."""

import warnings
from contextlib import contextmanager

import pandas as pd

from pandas_log import settings
from pandas_log.aop_utils import (
    create_overide_pandas_func,
    keep_pandas_func_copy,
    restore_pandas_func_copy,
)

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

    if verbose:
        settings.PANDAS_METHODS_TO_OVERIDE.extend(
            settings.PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
        )

    # Suppressing warning of the fact we override pandas functions.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for func in dir(pd.DataFrame):
            if func in settings.PANDAS_METHODS_TO_OVERIDE:
                keep_pandas_func_copy(func)
                create_overide_pandas_func(func, silent, full_signature)
    ALREADY_ENABLED = True


if __name__ == "__main__":
    pass
