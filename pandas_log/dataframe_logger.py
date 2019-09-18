from functools import partial

from pandas_log.aop_utils import get_patch_log_func, get_signature_repr


class DataFrameLogger:
    def __init__(
        self,
        exec_time,
        fn,
        fn_args,
        fn_kwargs,
        input_df,
        output_df,
        silent,
        full_signature,
        **kwargs,
    ):
        """ Constructor

            :param exec_time: the time it took a function to run in a human friendly way
            :param fn: The original pandas method
            :param fn_args: The original pandas method args
            :param fn_kwargs: The original pandas method kwargs
            :param input_df: the DataFrame before applying function fn
            :param output_df: the DataFrame after applying function fn
            :param silent: Whether additional the statistics get printed
        """

        # Behavioural variables
        self.silent = silent

        # Statistics variables
        self.exec_time = exec_time
        self.func_sig = get_signature_repr(fn, fn_args, full_signature)
        self.func_logs = None
        prev_step_number = DataFrameLogger.get_df_attr(
            input_df, "execution_step_number", 0
        )
        self.step_number = prev_step_number + 1

        # Persistence Variables
        DataFrameLogger.set_df_attr(
            output_df, "execution_step_number", self.step_number
        )
        prev_exec_history = DataFrameLogger.get_df_attr(
            input_df, "execution_history", []
        )
        DataFrameLogger.set_df_attr(
            output_df, "execution_history", prev_exec_history
        )
        self.output_df = output_df
        self.input_df = input_df

        # Variable to allow original method to run
        self.fn_args = fn_args
        self.fn = fn
        fn_kwargs["kwargs"] = fn_kwargs.copy()
        self.fn_kwargs = fn_kwargs

    @staticmethod
    def set_df_attr(df, attr_name, attr_value):
        """ Hacky way to set attributes in dataframe

            :param df: DataFrame
            :param attr_name: Attribute name
            :param attr_value: Attribute value
            :return: None
        """

        df.__dict__[attr_name] = attr_value

    @staticmethod
    def append_df_attr(df, attr_name, attr_value):
        """ Hacky way to append a value to dataframe

            :param df: DataFrame
            :param attr_name: Attribute name
            :param attr_value: Attribute value
            :return: None
        """

        df.__dict__[attr_name].append(attr_value)

    @staticmethod
    def get_df_attr(df, attr_name, default_val):
        """ Get Dataframe attribute if exists otherwise default value

            :return: Dataframe attribute
        """

        return df.__dict__.get(attr_name, default_val)

    def calc_step_stats(self):
        """Calculate relevant statistics for this pandas method and
           save an attribute (step_logs) which saves history of teh applied methods

           :return: None
        """

        log_method = get_patch_log_func(self.fn)
        log_method = partial(log_method, self.output_df, self.input_df)
        self.func_logs = log_method(*self.fn_args, **self.fn_kwargs)

        DataFrameLogger.append_df_attr(
            self.output_df, "execution_history", self
        )

        if not self.silent:
            print(self)

    def __repr__(self):
        """ Return string representation of DataFrameLogger aka
            Statistics regarding applied function

            :return: string representation of DataFrameLogger
        """

        func_logs = f"\n{self.func_logs}" if self.func_logs else ""
        return f"\n{self.step_number}) {self.func_sig}{func_logs}\n{self.exec_time}"
