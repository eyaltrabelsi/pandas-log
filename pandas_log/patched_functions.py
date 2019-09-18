from pandas_log.utils import *

QUERY_NO_FILTERED_ROWS_MSG = (
    "query:       * using expression '{predicate}' removed no rows"
)
QUERY_FILTERED_ROWS_MSG = "query:       * using expression '{predicate}' removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
NOT_IMPLEMENTED_MSG = "Log not implemented yet for this function"
DROPNA_NO_COLS_MSG = "dropna:      * removed no columns"
DROPNA_COLS_MSG = "dropna:      * removed the following columns {cols_removed)}\n               now only have the following columns {cols_remaining}"
FILLNA_NO_NA_MSG = "fillna:      * there are no nulls"
FILLNA_WITHH_NA_MSG = "fillna:      * filled {num_of_na} with {}"
DROPNA_NO_ROWS_MSG = "             * removed no rows"
DROPNA_ROWS_MSG = "             * removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
DROP_NO_COLS_MSG = "drop:        * removed no columns"
DROP_COLS_MSG = "drop:        * removed the following columns {cols_removed)}\n               now only have the following columns {cols_remaining}"
DROP_NO_ROWS_MSG = "             * removed no rows"
DROP_ROWS_MSG = "             * removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining"
ASSIGN_MSG = "assign:      * The columns {existing_cols} were reassigned\n             * The columns {new_cols} were created"
INDEX_RESET_MSG = "reset_index: *  The dataframe index been reset"
SORT_VALUES_MSG = "sort_values: *  sorting by columns {by} in a {'ascending' if ascending else 'descending'} order"
SORT_INDEX_MSG = "sort_index:  *  sorting by index in a {'ascending' if ascending else 'descending'} order"
HEAD_MSG = "head:        *  Picked the first {n} rows"
TAIL_MSG = "tail:        * Picked the last {n} rows"
JOIN_NO_ROWS_MSG = "{how} join:  * There is no change to number of rows"
JOIN_ROWS_MSG = (
    "{how} join:  * Number of rows changed, after join is {output_rows} rows"
)
JOIN_NEW_COLS_MSG = (
    "             * added {num_new_columns} columns ({new_columns})"
)
SAMPLE_MSG = "sample:      * picked random sample of {output_rows} rows"
NLARGEST_MSG = "nlargest:    * picked {n} largest rows by columns {cols}"
NSMALLEST_MSG = "nsmallest:   * picked {n} smallest rows by columns {cols}"


def _log_drop(df, output_df):
    if is_same_cols(df, output_df):
        print(DROP_NO_COLS_MSG)
    else:
        print(
            DROP_COLS_MSG.format(
                cols_removed=cols_removed(df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(df, output_df):
        print(DROP_NO_ROWS_MSG)
    else:
        print(
            DROP_ROWS_MSG.format(
                rows_removed=rows_removed(df, output_df),
                rows_removed_pct=rows_removed_pct(df, output_df),
                rows_remaining=rows_removed_pct(output_df),
            )
        )


def _log_dropna(df, output_df):
    if is_same_cols(df, output_df):
        print(DROPNA_NO_COLS_MSG)
    else:
        print(
            DROPNA_COLS_MSG.format(
                cols_removed=cols_removed(df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if is_same_rows(df, output_df):
        print(DROPNA_NO_ROWS_MSG)
    else:
        print(
            DROPNA_ROWS_MSG.format(
                rows_removed=rows_removed(df, output_df),
                rows_removed_pct=rows_removed_pct(df, output_df),
                rows_remaining=rows_removed_pct(output_df),
            )
        )


def _log_assign(df, assign_cols):
    print(
        ASSIGN_MSG.format(
            existing_cols=",".join(
                col
                for col in assign_cols
                if col in col in set(df.columns)
            ),
            new_cols=",".join(
                col
                for col in assign_cols
                if col not in col in set(df.columns)
            ),
        )
    )


def _log_query(df, output_df, expr):
    if is_same_rows(df, output_df):
        print(QUERY_NO_FILTERED_ROWS_MSG.format(predicate=expr))
    else:
        print(
            QUERY_FILTERED_ROWS_MSG.format(
                predicate=expr,
                rows_removed=rows_removed(df, output_df),
                rows_removed_pct=rows_removed_pct(df, output_df),
                rows_remaining=rows_removed_pct(df, output_df),
            )
        )


def _log_reset_index():
    print(INDEX_RESET_MSG)


def _log_sort_index(ascending):
    print(SORT_INDEX_MSG.format(ascending))


def _log_sort_values(by, ascending):
    print(SORT_VALUES_MSG.format(by, ascending))


def _log_tail(n):
    print(TAIL_MSG.format(n))


def _log_head(n):
    print(HEAD_MSG.format(n))


def _log_merge(df, other_df, output_df, how):
    if is_same_rows(df, output_df):
        print(JOIN_NO_ROWS_MSG.format(how=how))
    else:
        print(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(df, output_df):
        print(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(df, other_df),
                new_columns=str_new_columns(df, other_df),
            )
        )


def _log_join(df, other_df, output_df, how):
    if is_same_rows(df, output_df):
        print(JOIN_NO_ROWS_MSG.format(how=how))
    else:
        print(JOIN_ROWS_MSG.format(how=how, output_rows=len(output_df)))
    if not is_same_cols(df, output_df):
        print(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(df, other_df),
                new_columns=str_new_columns(df, other_df),
            )
        )


def _log_fillna(df, output_df):
    if num_of_na(df) == num_of_na(output_df):
        print(FILLNA_NO_NA_MSG)
    else:
        print(FILLNA_WITHH_NA_MSG.format(num_of_na=num_of_na(df)))


def _log_sample(output_df):
    print(SAMPLE_MSG.format(output_rows=len(output_df)))


def _log_nlargest(n, columns):
    print(NLARGEST_MSG.format(n=n, cols=",".join(columns)))


def _log_nsmallest(n, columns):
    print(NSMALLEST_MSG.format(n=n, cols=",".join(columns)))


def _log_shift(df, output_df):
    print(NOT_IMPLEMENTED_MSG)


def _log_melt(df, output_df):
    print(NOT_IMPLEMENTED_MSG)


# TODO iloc, loc, ix ,
# todo apply applymap pipe
# todo where  isin mask
# TODO rolling, groupby, .rename   expanding explode

if __name__ == "__main__":
    pass
