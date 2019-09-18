from time import time


class Timer:
    def __enter__(self):
        self.start = time()
        return self

    def __exit__(self, *args):
        self.end = time()
        self.interval = self.end - self.start


def get_existing_methods_names(module, prefix):
    return [func for func in dir(__import__(module))
            if func.startswith(prefix)]


def rows_removed(input_df, output_df):
    return len(input_df) - len(output_df)


def rows_removed_pct(input_df, output_df):
    return (len(input_df) - len(output_df)) / len(input_df)


def rows_remaining(output_df):
    return len(output_df)


def cols_removed(input_df, output_df):
    return ",".join(set(input_df.columns) - set(output_df.columns))


def cols_remaining(output_df):
    return ",".join(set(output_df.columns))


def is_same_cols(input_df, output_df):
    return len(input_df.columns) == len(output_df.columns)


def is_same_rows(input_df, output_df):
    return len(input_df) == len(output_df)


def num_of_na(df):
    return len(df) - df.count()


def str_new_columns(input_df, output_df):
    return ",".join(set(output_df.columns) - set(input_df.columns))


def num_new_columns(input_df, output_df):
    return len(set(output_df.columns) - set(input_df.columns))


if __name__ == "__main__":
    pass
