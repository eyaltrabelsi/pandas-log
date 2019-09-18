from pandas_log.utils import *

REMOVED_NO_ROWS_MSG = "\t* Removed no rows."
REMOVED_NO_COLS_MSG = "\t* removed no columns"
QUERY_FILTERED_ROWS_MSG = "\t* Removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
NOT_IMPLEMENTED_MSG = "\t*Log not implemented yet for this function"
DROPNA_COLS_MSG = "\t* removed the following columns {cols_removed)} now only have the following columns {cols_remaining}"
FILLNA_NO_NA_MSG = "\t* there are no nulls"
FILLNA_WITHH_NA_MSG = "\t* filled {num_of_na} with {}"
DROPNA_ROWS_MSG = "\t* removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
DROP_COLS_MSG = "\t* removed the following columns {cols_removed)}\n\t*now only have the following columns {cols_remaining}"
DROP_ROWS_MSG = "\t* removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
ASSIGN_EXISTING_MSG = "\t* The columns {existing_cols} were reassigned"
ASSIGN_NEW_MSG = "\t* The columns {new_cols} were created"
SORT_VALUES_MSG = "\t* sorting by columns {by} in a {'ascending' if ascending else 'descending'} order"
SORT_INDEX_MSG = "\t* sorting by index in a {'ascending' if ascending else 'descending'} order"
HEAD_MSG = "\t* Picked the first {n} rows"
TAIL_MSG = "\t* Picked the last {n} rows"
JOIN_NO_ROWS_MSG = (
    "\t* Its a {how} join.\n\t* There is no change to number of rows"
)
JOIN_ROWS_MSG = "\t* Its a {how} join.\n\t* Number of rows changed, after join is {output_rows} rows"
JOIN_NEW_COLS_MSG = "\t* added {num_new_columns} columns ({new_columns})"
SAMPLE_MSG = "\t* picked random sample of {output_rows} rows"
NLARGEST_MSG = "\t* picked {n} largest rows by columns {cols}"
NSMALLEST_MSG = "\t* picked {n} smallest rows by columns {cols}"


def _log_drop(df, output_df, **kwargs):
    logs = []
    if is_same_cols(df, output_df):
        logs.append(REMOVED_NO_COLS_MSG)
    else:
        logs.append(
            DROP_COLS_MSG.format(
                cols_removed=cols_removed(df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(
            DROP_ROWS_MSG.format(
                rows_removed=rows_removed(df, output_df),
                rows_removed_pct=rows_removed_pct(df, output_df),
                rows_remaining=rows_removed_pct(output_df),
            )
        )
    return "\n".join(logs)


def _log_dropna(df, output_df, **kwargs):
    logs = []
    if is_same_cols(df, output_df):
        logs.append(REMOVED_NO_COLS_MSG)
    else:
        logs.append(
            DROPNA_COLS_MSG.format(
                cols_removed=cols_removed(df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(
            DROPNA_ROWS_MSG.format(
                rows_removed=rows_removed(df, output_df),
                rows_removed_pct=rows_removed_pct(df, output_df),
                rows_remaining=rows_removed_pct(df, output_df),
            )
        )
    return "\n".join(logs)


def _log_assign(df, kwargs, **other_kwargs):
    logs = []
    cols = kwargs.keys()
    if columns_changed(df, cols):
        logs.append(
            ASSIGN_EXISTING_MSG.format(
                existing_cols=",".join(columns_changed(df, cols))
            )
        )
    if columns_added(df, cols):
        logs.append(
            ASSIGN_NEW_MSG.format(new_cols=",".join(columns_added(df, cols)))
        )
    return "\n".join(logs)


def _log_query(output_df, df, **kwargs):
    if is_same_rows(df, output_df):
        return REMOVED_NO_ROWS_MSG
    else:
        return QUERY_FILTERED_ROWS_MSG.format(
            rows_removed=rows_removed(df, output_df),
            rows_removed_pct=rows_removed_pct(df, output_df),
            rows_remaining=rows_removed_pct(df, output_df),
        )


def _log_reset_index(**kwargs):
    return ""


def _log_sort_index(ascending, **kwargs):
    return SORT_INDEX_MSG.format(ascending)


def _log_sort_values(by, ascending, **kwargs):
    return SORT_VALUES_MSG.format(by, ascending)


def _log_tail(n, **kwargs):
    return TAIL_MSG.format(n)


def _log_head(n):
    return HEAD_MSG.format(n)


def _log_merge(df, other_df, output_df, how, **kwargs):
    logs = []
    if is_same_rows(df, output_df):
        logs.append(JOIN_NO_ROWS_MSG.format(how=how))
    else:
        logs.append(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(df, other_df),
                new_columns=str_new_columns(df, other_df),
            )
        )
    return "\n".join(logs)


def _log_join(df, other_df, output_df, how, **kwargs):
    logs = []
    if is_same_rows(df, output_df):
        logs.append(JOIN_NO_ROWS_MSG.format(how=how))
    else:
        logs.append(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(df, other_df),
                new_columns=str_new_columns(df, other_df),
            )
        )
    return logs


def _log_fillna(df, output_df, **kwargs):
    if num_of_na(df) == num_of_na(output_df):
        return FILLNA_NO_NA_MSG
    else:
        return FILLNA_WITHH_NA_MSG.format(num_of_na=num_of_na(df))


def _log_sample(output_df, **kwargs):
    return SAMPLE_MSG.format(output_rows=len(output_df))


def _log_nlargest(output_df, columns, **kwargs):
    return NLARGEST_MSG.format(n=len(output_df), cols=",".join(columns))


def _log_nsmallest(output_df, columns, **kwargs):
    return NSMALLEST_MSG.format(n=len(output_df), cols=",".join(columns))


def _log_shift(output_df, **kwargs):
    return NOT_IMPLEMENTED_MSG


def _log_melt(output_df, **kwargs):
    return NOT_IMPLEMENTED_MSG


# TODO iloc, loc, ix ,
# todo apply applymap pipe
# todo where  isin mask
# TODO rolling, groupby, .rename   expanding explode

if __name__ == "__main__":
    pass
