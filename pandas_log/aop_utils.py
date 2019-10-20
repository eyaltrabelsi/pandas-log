import itertools
from contextlib import suppress
from functools import partial, wraps
from inspect import signature

import pandas as pd

import pandas_flavor as pf
from pandas_log import patched_logs_functions, settings
from pandas_log.timer import Timer


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


def get_pandas_func(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Get original pandas method

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: Original pandas method
    """

    return getattr(pd.DataFrame, f"{prefix}{func.__name__}")


def get_signature_repr(fn, args, full_signature=True):
    """ Get the signature for the original pandas method with actual values

        :param fn: The pandas method
        :param args: The arguments used when it was applied
        :return: string representation of the signature for the applied pandas method
    """

    def _get_bold_text(text):
        return f"\033[1m{text}\033[0m"

    def _get_orig_func_params():
        return [
            param_value if full_signature else param_name
            for param_name, param_value in signature(
                get_pandas_func(fn)
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
                if isinstance(arg_value, pd.DataFrame)
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


def get_patch_log_func(func, prefix=settings.PATCHED_LOG_METHOD_PREFIX):
    """ Get return relevant log function.
        For example: for .query pandas' method as input one will get ._log_query method
        from patched_functions

        :param func: The pandas method we applied and going to calculate stats
        :return: a function which calculate statistic for the applied pandas method
    """

    log_method = getattr(patched_logs_functions, "log_default")
    with suppress(AttributeError):
        log_method = getattr(
            patched_logs_functions, f"{prefix}{func.__name__}"
        )

    return log_method


def restore_pandas_func_copy(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Restore the original pandas method instead of overridden one

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, func.replace(prefix, ""), original_method)


def keep_pandas_func_copy(func, prefix=settings.ORIGINAL_METHOD_PREFIX):
    """ Saved copy of the pandas method before it overridden

        :param func: pandas method name
        :param prefix: the prefix used to keep original method
        :return: None
    """

    original_method = getattr(pd.DataFrame, func)
    setattr(pd.DataFrame, f"{prefix}{func}", original_method)


def create_overide_pandas_func(func, silent, full_signature):
    """ Create overridden pandas method dynamically with
        additional logging using DataFrameLogger

        Note: if we extracting _overide_dataframe_method outside we need to implement decorator like here
              https://stackoverflow.com/questions/10176226/how-do-i-pass-extra-arguments-to-a-python-decorator

        :param func: pandas method name to be overridden
        :param silent: Whether additional the statistics get printed
        :param full_signature: adding additional information to function signature
        :return: the same function with additional logging capabilities
    """

    def _get_step_stats(
        fn, fn_args, fn_kwargs, input_df, output_df, exec_time, step_number
    ):
        from pandas_log.step_stats import StepStats

        func_logs = _get_logs_for_specifc_method(
            fn, fn_args, fn_kwargs, input_df, output_df
        )

        step_stats = StepStats(
            exec_time, fn, fn_args, full_signature, step_number, func_logs
        )
        return step_stats

    def _persist_execution_stats(input_df, output_df, step_stats, step_number):
        set_df_attr(output_df, "execution_step_number", step_number)
        prev_exec_history = get_df_attr(input_df, "execution_history", [])
        set_df_attr(output_df, "execution_history", prev_exec_history)
        append_df_attr(output_df, "execution_history", step_stats)

    def _get_logs_for_specifc_method(
        fn, fn_args, fn_kwargs, input_df, output_df
    ):
        fn_kwargs["kwargs"] = fn_kwargs.copy()
        log_method = get_patch_log_func(fn)
        log_method = partial(log_method, output_df, input_df)
        return log_method(*fn_args, **fn_kwargs)

    def _overide_dataframe_method(fn):
        @pf.register_dataframe_method
        @wraps(fn)
        def wrapped(*args, **fn_kwargs):
            # Execute original method and save execution time in t
            with Timer() as t:
                output_df = get_pandas_func(fn)(*args, **fn_kwargs)

            # Prepare variables
            input_df, fn_args, exec_time = args[0], args[1:], t.exec_time
            step_number = get_df_attr(input_df, "execution_step_number", 0) + 1

            # calculate steps stats and persist them into the dataframes
            step_stats = _get_step_stats(
                fn,
                fn_args,
                fn_kwargs,
                input_df,
                output_df,
                exec_time,
                step_number,
            )
            _persist_execution_stats(
                input_df, output_df, step_stats, step_number
            )

            if not silent:
                print(step_stats)

            return output_df

        return wrapped

    return exec(
        f"@_overide_dataframe_method\ndef {func}(df, *args, **kwargs): pass"
    )


if __name__ == "__main__":
    pass
