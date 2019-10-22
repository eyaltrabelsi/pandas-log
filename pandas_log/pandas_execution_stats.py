import warnings
from time import time

from pandas_log.settings import PANDAS_ADDITIONAL_METHODS_TO_OVERIDE

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import humanize


class PandasExecutionStats:
    @staticmethod
    def get_humanized_exec_time(end, start):
        """ Return the time it took a function to run in a human friendly way

            :param end: time exactly after method was applied
            :param start: time right before method was applied
            :return: execution time in human friendly way
        """

        exec_time = end - start
        exec_time_humanize = humanize.naturaldelta(exec_time)
        if exec_time_humanize == "a moment":
            exec_time_humanize = f"{exec_time} seconds."
        return exec_time_humanize

    def __enter__(self, *args, **kwargs):
        self.start = time()
        return self

    def __exit__(self, *args, **kwargs):
        self.exec_time = PandasExecutionStats.get_humanized_exec_time(
            end=time(), start=self.start
        )
        self.memory_size = "TODO"


#             memory_size = output_df.memory_usage(index=True, deep=True)
#         memory_size = humanize.naturalsize(memory_size.sum()) if isinstance(memory_size, pd.Series) else humanize.naturalsize(memory_size)


class StepStats:
    def __init__(
        self,
        execution_stats,
        fn,
        fn_args,
        full_signature,
        step_number,
        func_logs=None,
    ):
        """ Constructor
            :param execution_stats: execution_stats of the pandas operation both in time and memory
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param full_signature: adding additional information to function signature
            :param step_number: number of of operation in sequence
            :param func_logs: additional logs
        """

        self.execution_stats = execution_stats
        from pandas_log.aop_utils import get_signature_repr

        self.func_sig = get_signature_repr(fn, fn_args, full_signature)
        self.func_logs = func_logs
        self.step_number = step_number
        self.fn = fn

    def __repr__(self):
        """ Return string representation of DataFrameLogger aka
            Statistics regarding applied function

            :return: string representation of StepStats
        """

        func_logs = f"{self.func_logs}" if self.func_logs else ""
        step_number = (
            "X"
            if self.fn.__name__ in PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
            else self.step_number
        )
        exec_time_humanize = (
            f"* Execution time: Step Took {self.execution_stats.exec_time}."
        )
        exec_memory_humanize = (
            f"* Output Dataframe size: {self.execution_stats.memory_size}."
        )
        return f"\n{step_number}) {self.func_sig}\n\tMetadata:\n{func_logs}\n\tExecution Stats:\n\t{exec_time_humanize}\n\t{exec_memory_humanize}"


if __name__ == "__main__":
    pass
