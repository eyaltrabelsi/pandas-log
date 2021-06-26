import itertools
from inspect import signature

import pandas as pd

from pandas_log import settings
from pandas_log.settings import DATAFRAME_ADDITIONAL_METHODS_TO_OVERIDE


def set_df_attr(df, attr_name, attr_value):
    """ Hacky way to set attributes in dataframe

        :param df: DataFrame
        :param attr_name: Attribute name
        :param attr_value: Attribute value
        :return: None
    """

    df.__dict__[attr_name] = attr_value


def append_df_attr(df, attr_name, attr_value):
    """ Hacky way to append a value to dataframe

        :param df: DataFrame
        :param attr_name: Attribute name
        :param attr_value: Attribute value
        :return: None
    """

    df.__dict__[attr_name].append(attr_value)


def get_df_attr(df, attr_name, default_val):
    """ Get Dataframe attribute if exists otherwise default value

        :return: Dataframe attribute
    """

    return df.__dict__.get(attr_name, default_val)


def get_pandas_func(cls, func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Get original pandas method

        :param cls: pandas class
        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: Original pandas method
    """

    _raise_on_bad_class(cls)
    return getattr(cls, f"{prefix}{func.__name__}")


def get_signature_repr(cls, fn, args, full_signature=True):
    """ Get the signature for the original pandas method with actual values

        :param cls: the pandas class
        :param fn: The pandas method
        :param args: The arguments used when it was applied
        :return: string representation of the signature for the applied pandas method
    """

    _raise_on_bad_class(cls)

    def _get_bold_text(text):
        return f"\033[1m{text}\033[0m"

    def _get_orig_func_params():
        return [
            param_value if full_signature else param_name
            for param_name, param_value in signature(
                get_pandas_func(cls, fn)
            ).parameters.items()
            if param_name not in ("kwargs", "self")
        ]

    def _get_param_value(param_with_default, arg_value):
        res = str(param_with_default)
        if arg_value is not None:
            param_name = res.split("=")[0]
            arg_value = (
                f'"{arg_value}"' if isinstance(arg_value, str) else arg_value
            )
            res = (
                param_name
                if isinstance(arg_value, (pd.DataFrame, pd.Series))
                else f"{param_name}={arg_value}"
            )

        return res

    zip_func = itertools.zip_longest if full_signature else zip
    orig_func_params = _get_orig_func_params()
    args_vals = ", ".join(
        _get_param_value(param_with_default, arg_value)
        for param_with_default, arg_value in zip_func(orig_func_params, args)
    )
    return f"{_get_bold_text(fn.__name__)}({args_vals}):"


def _raise_on_bad_class(cls):
    implemented_classes = (pd.DataFrame, pd.Series)
    if cls not in implemented_classes:
        raise TypeError("cls must be one of {}".format(implemented_classes))


def restore_pandas_func_copy(
    cls, func, prefix=settings.ORIGINAL_METHOD_PREFIX
):
    """ Restore the original pandas method instead of overridden one

        :param cls: class containing the method
        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    _raise_on_bad_class(cls)
    original_method = getattr(cls, func)
    setattr(cls, func.replace(prefix, ""), original_method)


def keep_pandas_func_copy(cls, func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Saved copy of the pandas method before it overridden

        :param cls: class containing the method
        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    _raise_on_bad_class(cls)
    original_method = getattr(cls, func)
    setattr(cls, f"{prefix}{func}", original_method)


def calc_step_number(method_name, input_df):
    # TODO
    step_number = get_df_attr(input_df, "execution_history", 0)
    if step_number:
        step_number = step_number[-1].execution_stats.step_number

    if method_name not in DATAFRAME_ADDITIONAL_METHODS_TO_OVERIDE:
        step_number += 1
    return step_number


pass
