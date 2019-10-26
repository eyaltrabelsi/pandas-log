import warnings
from collections import namedtuple
from contextlib import suppress
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
    PANDAS_ADDITIONAL_METHODS_TO_OVERIDE,
    PATCHED_LOG_METHOD_PREFIX,
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import humanize


def get_execution_stats(fn, input_df, fn_args, fn_kwargs):
    start = time()
    output_df = get_pandas_func(fn)(input_df, *fn_args, **fn_kwargs)
    exec_time = humanize.naturaldelta(time() - start)
    if exec_time == "a moment":
        exec_time = f"{exec_time} seconds."
    step_number = calc_step_number(fn.__name__, input_df)

    input_memory_size = StepStats.calc_df_series_memory(input_df)
    output_memory_size = StepStats.calc_df_series_memory(output_df)

    ExecutionStats = namedtuple(
        "ExecutionStats",
        "exec_time step_number input_memory_size output_memory_size",
    )
    execution_stats = ExecutionStats(
        exec_time, step_number, input_memory_size, output_memory_size
    )
    return output_df, execution_stats


class StepStats:
    def __init__(
        self,
        execution_stats,
        fn,
        fn_args,
        fn_kwargs,
        full_signature,
        input_df,
        output_df,
    ):
        """ Constructor
            :param execution_stats: execution_stats of the pandas operation both in time and memory
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param fn_kwargs: The original pandas method kwargs
            :param full_signature: adding additional information to function signature
            :param input_df: dataframe before step calculation
            :param output_df: dataframe after step calculation
        """

        self.execution_stats = execution_stats
        self.full_signature = full_signature
        self.fn = fn
        self.fn_args = fn_args
        self.fn_kwargs = fn_kwargs
        self.input_df = input_df
        self.output_df = output_df

    @staticmethod
    def calc_df_series_memory(df_or_series):
        memory_size = df_or_series.memory_usage(index=True, deep=True)
        return (
            humanize.naturalsize(memory_size.sum())
            if isinstance(memory_size, pd.Series)
            else humanize.naturalsize(memory_size)
        )

    def persist_execution_stats(self):
        prev_exec_history = get_df_attr(self.input_df, "execution_history", [])
        set_df_attr(self.output_df, "execution_history", prev_exec_history)
        append_df_attr(self.output_df, "execution_history", self)

    def log_stats_if_needed(self, silent, verbose):

        from pandas_log.pandas_log import ALREADY_ENABLED

        if silent or not ALREADY_ENABLED:
            return

        if (
            verbose
            or self.fn.__name__ not in PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
        ):
            print(self)

    def get_logs_for_specifc_method(self):
        self.fn_kwargs["kwargs"] = self.fn_kwargs.copy()
        log_method = getattr(patched_logs_functions, "log_default")
        with suppress(AttributeError):
            log_method = getattr(
                patched_logs_functions,
                f"{PATCHED_LOG_METHOD_PREFIX}{self.fn.__name__}",
            )

        log_method = partial(log_method, self.output_df, self.input_df)
        return log_method(*self.fn_args, **self.fn_kwargs)

    def __repr__(self):
        # Step title
        func_sig = get_signature_repr(
            self.fn, self.fn_args, self.full_signature
        )
        step_number = (
            "X"
            if self.fn.__name__ in PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
            else self.execution_stats.step_number
        )
        step_title = f"{step_number}) {func_sig}"

        # Step Metadata stats
        func_logs = self.get_logs_for_specifc_method()
        metadata_stats = (
            f"\033[4mMetadata\033[0m:\n{func_logs}"
            if func_logs
            else "Metadata:\n"
        )

        # Step Execution stats
        exec_time_humanize = (
            f"* Execution time: Step Took {self.execution_stats.exec_time}."
        )
        exec_input_memory_humanize = f"* Input Dataframe size is {self.execution_stats.input_memory_size}."
        exec_output_memory_humanize = f"* Output Dataframe size is {self.execution_stats.output_memory_size}."
        execution_stats = f"\033[4mExecution Stats\033[0m:\n\t{exec_time_humanize}\n\t{exec_input_memory_humanize}\n\t{exec_output_memory_humanize}"

        return f"\n{step_title}\n\t{metadata_stats}\n\t{execution_stats}"


if __name__ == "__main__":
    pass
