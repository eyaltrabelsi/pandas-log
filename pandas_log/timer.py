import warnings
from time import time

# TODO should fork humanize for cleaner Timer interface or to extract
# TODO this class to a small useful package

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import humanize


class Timer:
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
        return f"\t* Step Took {exec_time_humanize}"

    def __enter__(self, *args, **kwargs):
        self.start = time()
        return self

    def __exit__(self, *args, **kwargs):
        self.exec_time = Timer.get_humanized_exec_time(
            end=time(), start=self.start
        )


if __name__ == "__main__":
    pass
