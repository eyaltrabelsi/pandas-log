import warnings
from collections import namedtuple
from functools import partial
from time import time

import pandas as pd

from pandas_log import patched_logs_functions
from pandas_log.aop_utils import (
    append_df_attr,
    calc_step_number,
    get_df_attr,
    get_pandas_func,
    get_signature_repr,
    set_df_attr,
)
from pandas_log.settings import (
    DATAFRAME_ADDITIONAL_METHODS_TO_OVERIDE,
    PATCHED_LOG_METHOD_PREFIX,
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import humanize


def get_execution_stats(cls, fn, input_df, fn_args, fn_kwargs, calculate_memory):
    start = time()
    output_df = get_pandas_func(cls, fn)(input_df, *fn_args, **fn_kwargs)
    exec_time = time() - start
    exec_time_pretty = humanize.naturaldelta(exec_time)
    if exec_time_pretty == "a moment":
        exec_time_pretty = f"{round(exec_time,6)} seconds"
    step_number = calc_step_number(fn.__name__, input_df)

    input_memory_size = (
        StepStats.calc_df_series_memory(input_df) if calculate_memory else None
    )
    output_memory_size = (
        StepStats.calc_df_series_memory(output_df) if calculate_memory else None
    )

    ExecutionStats = namedtuple(
        "ExecutionStats", "exec_time step_number input_memory_size output_memory_size",
    )
    execution_stats = ExecutionStats(
        exec_time_pretty, step_number, input_memory_size, output_memory_size
    )
    return output_df, execution_stats


class StepStats:
    def __init__(
        self,
        execution_stats,
        cls,
        fn,
        fn_args,
        fn_kwargs,
        full_signature,
        input_df,
        output_df,
    ):
        """ Constructor
            :param execution_stats: execution_stats of the pandas operation both in time and memory
            :param cls: The calling object's pandas class
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param fn_kwargs: The original pandas method kwargs
            :param full_signature: adding additional information to function signature
            :param input_df: dataframe before step calculation
            :param output_df: dataframe after step calculation
        """

        self.execution_stats = execution_stats
        self.full_signature = full_signature
        self.cls = cls
        self.fn = fn
        self.fn_args = fn_args
        self.fn_kwargs = fn_kwargs
        self.input_df = input_df
        self.output_df = output_df

    @staticmethod
    def calc_df_series_memory(df_or_series):
        res = None
        if isinstance(df_or_series, pd.Series):
            mem = df_or_series.memory_usage(index=True, deep=True)
            res = humanize.naturalsize(mem)
        elif isinstance(df_or_series, pd.DataFrame):
            mem = df_or_series.memory_usage(index=True, deep=True)
            res = humanize.naturalsize(mem.sum())
        return res

    def persist_execution_stats(self):
        prev_exec_history = get_df_attr(self.input_df, "execution_history", [])
        set_df_attr(self.output_df, "execution_history", prev_exec_history)
        append_df_attr(self.output_df, "execution_history", self)

    def log_stats_if_needed(self, silent, verbose, copy_ok):

        from pandas_log.pandas_log import ALREADY_ENABLED

        if silent or not ALREADY_ENABLED:
            return

        if verbose or self.fn.__name__ not in DATAFRAME_ADDITIONAL_METHODS_TO_OVERIDE:
            s = self.__repr__(verbose, copy_ok)
            if s:
                # If this method isn't patched and verbose is False, __repr__ will give an empty string, which
                # we don't want to print
                print(s)

    def get_logs_for_specifc_method(self, verbose, copy_ok):
        self.fn_kwargs["kwargs"] = self.fn_kwargs.copy()
        self.fn_kwargs["copy_ok"] = copy_ok
        try:
            log_method = getattr(
                patched_logs_functions,
                f"{PATCHED_LOG_METHOD_PREFIX}{self.fn.__name__}",
            )
        except AttributeError:
            # Method is listed as a method to override, but no patched function exists
            if verbose:
                log_method = getattr(patched_logs_functions, "log_default")
            else:
                log_method = getattr(patched_logs_functions, "log_no_message")

        log_method = partial(log_method, self.output_df, self.input_df)
        logs, tips = log_method(*self.fn_args, **self.fn_kwargs)
        return logs, tips

    def _repr_html_(self):
        pass

    def __repr__(self, verbose, copy_ok):
        # Step title
        func_sig = get_signature_repr(
            self.cls, self.fn, self.fn_args, self.full_signature
        )
        step_number = (
            "X"
            if self.fn.__name__ in DATAFRAME_ADDITIONAL_METHODS_TO_OVERIDE
            else self.execution_stats.step_number
        )
        step_title = f"{step_number}) {func_sig}"

        # Step Metadata stats
        logs, tips = self.get_logs_for_specifc_method(verbose, copy_ok)
        metadata_stats = f"\033[4mMetadata\033[0m:\n{logs}" if logs else ""
        metadata_tips = f"\033[4mTips\033[0m:\n{tips}" if tips else ""

        # Step Execution stats
        exec_time_humanize = (
            f"* Execution time: Step Took {self.execution_stats.exec_time}."
        )
        exec_stats_raw = [exec_time_humanize]
        if self.execution_stats.input_memory_size is not None:
            exec_stats_raw.append(
                f"* Input Dataframe size is {self.execution_stats.input_memory_size}."
            )
        if self.execution_stats.output_memory_size is not None:
            exec_stats_raw.append(
                f"* Output Dataframe size is {self.execution_stats.output_memory_size}."
            )
        exec_stats_raw_str = "\n\t".join(exec_stats_raw)
        execution_stats = f"\033[4mExecution Stats\033[0m:\n\t{exec_stats_raw_str}"

        all_logs = [metadata_stats, execution_stats, metadata_tips]
        all_logs_str = "\n\t".join([x for x in all_logs if x])

        return f"\n{step_title}\n\t{all_logs_str}"


if __name__ == "__main__":
    pass
