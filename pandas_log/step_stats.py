from pandas_log.aop_utils import get_signature_repr
from pandas_log.settings import PANDAS_ADDITIONAL_METHODS_TO_OVERIDE


class StepStats:
    def __init__(
        self,
        exec_time,
        fn,
        fn_args,
        full_signature,
        step_number,
        func_logs=None,
    ):
        """ Constructor

            :param exec_time: the time it took a function to run in a human friendly way
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param full_signature: adding additional information to function signature
            :param step_number: number of of operation in sequence
            :param func_logs: additional logs
        """

        self.exec_time = exec_time
        self.func_sig = get_signature_repr(fn, fn_args, full_signature)
        self.func_logs = func_logs
        self.step_number = step_number
        self.fn = fn

    def __repr__(self):
        """ Return string representation of DataFrameLogger aka
            Statistics regarding applied function

            :return: string representation of StepStats
        """

        func_logs = f"\n{self.func_logs}" if self.func_logs else ""
        step_number = (
            "X"
            if self.fn.__name__ in PANDAS_ADDITIONAL_METHODS_TO_OVERIDE
            else self.step_number
        )
        return f"\n{step_number}) {self.func_sig}{func_logs}\n{self.exec_time}"
