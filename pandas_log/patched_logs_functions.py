import pandas as pd

# Rows messages
REMOVED_NO_ROWS_MSG = "\t* No change in number of rows of input df."
FILTERED_ROWS_MSG = "\t* Removed {rows_removed} rows ({rows_removed_pct}%), {rows_remaining} rows remaining."

# Cols messages
REMOVED_NO_COLS_MSG = "\t* Removed no columns."
FILTERED_COLS_MSG = "\t* Removed the following columns ({cols_removed}) now only have the following columns ({cols_remaining})."
ASSIGN_EXISTING_MSG = "\t* The columns {existing_cols} were reassigned."
ASSIGN_NEW_MSG = "\t* The columns {new_cols} were created."

# Group by messages
GROUPBY_MSG = "\t* Grouping by {} resulted in {} groups like {}."
# N/A messages
FILLNA_NO_NA_MSG = "\t* There are no nulls."
FILLNA_WITHH_NA_MSG = "\t* Filled {} with {}."

# Mege messages
JOIN_ROWS_MSG = "\t* Number of rows changed, after join is {output_rows} rows."
JOIN_NEW_COLS_MSG = "\t* Added {num_new_columns} columns ({new_columns})."
JOIN_TYPE_MSG = "\t* Its a {how} join with the following cardinality:\n\t\t> rows only in left is {left_only}.\n\t\t> rows only in right is {right_only}.\n\t\t> rows in both is {both}."

# Pick messages
SAMPLE_MSG = "\t* Picked random sample of {output_rows} rows."
NLARGEST_MSG = "\t* Picked {n} largest rows by columns ({cols})."
NSMALLEST_MSG = "\t* Picked {n} smallest rows by columns ({cols})."
HEAD_MSG = "\t* Picked the first {} rows."
TAIL_MSG = "\t* Picked the last {} rows."


# TIPS
ITERROWS_TIPS = "\t*iterrows is not recommended, and in the majority of cases will have better alternatives"
FILLNA_NO_NA_TIP = "\t* There are no nulls in this dataframe, if you are working on the entire dataset you can remove this operation."
SHOULD_REDUCED_ROW_TIP = "\t* Number of rows didn't change, if you are working on the entire dataset you can remove this operation."

# Others
SORT_VALUES_MSG = "\t* Sorting by columns {by} in a {'ascending' if ascending else 'descending'} order."
SORT_INDEX_MSG = "\t* Sorting by index in a {'ascending' if ascending else 'descending'} order."
DEFAULT_STRATEGY_USED_MSG = (
    "\t* Using default strategy (some metric might not be relevant)."
)
TRANSFORMED_TO_DF_MSG = "\t* After transformation we received Series"


def rows_removed(input_df, output_df):
    return len(input_df) - len(output_df)


def rows_removed_pct(input_df, output_df):
    return 100 * (rows_removed(input_df, output_df)) / len(input_df)


def rows_remaining(output_df):
    return len(output_df)


def cols_removed(input_df, output_df):
    return ", ".join(set(input_df.columns) - set(output_df.columns))


def cols_remaining(output_df):
    return ", ".join(set(output_df.columns))


def is_same_cols(input_df, output_df):
    return len(input_df.columns) == len(output_df.columns)


def columns_changed(df, cols):
    return set(df.columns).intersection(set(cols))


def columns_added(df, cols):
    return set(cols) - set(df.columns)


def is_same_rows(input_df, output_df):
    return len(input_df) == len(output_df)


def num_of_na(df):
    return df.isnull().values.sum()


def str_new_columns(input_df, output_df):
    return ", ".join(set(output_df.columns) - set(input_df.columns))


def num_new_columns(input_df, output_df):
    return len(set(output_df.columns) - set(input_df.columns))


def get_filter_rows_logs(input_df, output_df):
    tips = ""
    if is_same_rows(input_df, output_df):
        logs = REMOVED_NO_ROWS_MSG
        tips = SHOULD_REDUCED_ROW_TIP
    else:
        logs = FILTERED_ROWS_MSG.format(
            rows_removed=rows_removed(input_df, output_df),
            rows_removed_pct=rows_removed_pct(input_df, output_df),
            rows_remaining=rows_remaining(output_df),
        )
    return logs, tips


def log_default(output_df, input_df, *args, **kwargs):
    logs = [DEFAULT_STRATEGY_USED_MSG]
    tips = ""
    if isinstance(output_df, pd.DataFrame):
        if not is_same_cols(input_df, output_df):
            logs.append(
                FILTERED_COLS_MSG.format(
                    cols_removed=cols_removed(input_df, output_df),
                    cols_remaining=cols_remaining(output_df),
                )
            )
        if not is_same_rows(input_df, output_df):
            logs.append(
                FILTERED_ROWS_MSG.format(
                    rows_removed=rows_removed(input_df, output_df),
                    rows_removed_pct=rows_removed_pct(input_df, output_df),
                    rows_remaining=rows_remaining(output_df),
                )
            )
    elif isinstance(output_df, pd.Series):
        logs.append(TRANSFORMED_TO_DF_MSG)
    logs = "\n".join(logs)
    return logs, tips


def log_drop(
    output_df,
    input_df,
    labels=None,
    axis=0,
    index=None,
    columns=None,
    level=None,
    inplace=False,
    errors="raise",
    *args,
    **kwargs,
):
    logs, tips = get_filter_rows_logs(input_df, output_df)
    tips = ""
    if is_same_cols(input_df, output_df):
        logs += f"\n{REMOVED_NO_COLS_MSG}"
    else:
        msg = FILTERED_COLS_MSG.format(
            cols_removed=cols_removed(input_df, output_df),
            cols_remaining=cols_remaining(output_df),
        )
        logs += f"\n{msg}"
    return logs, tips


def log_dropna(
    output_df,
    input_df,
    axis=0,
    how="any",
    thresh=None,
    subset=None,
    inplace=False,
    **kwargs,
):
    logs, tips = get_filter_rows_logs(input_df, output_df)
    if is_same_cols(input_df, output_df):
        logs += f"\n{REMOVED_NO_COLS_MSG}"
        tips = SHOULD_REDUCED_ROW_TIP
    else:
        msg = FILTERED_COLS_MSG.format(
            cols_removed=cols_removed(input_df, output_df),
            cols_remaining=cols_remaining(output_df),
        )
        logs += f"\n{msg}"
    return logs, tips


def log_assign(output_df, input_df, **kwargs):
    logs = []
    tips = ""
    cols = kwargs.keys()
    if columns_changed(input_df, cols):
        logs.append(
            ASSIGN_EXISTING_MSG.format(
                existing_cols=", ".join(columns_changed(input_df, cols))
            )
        )
    if columns_added(input_df, cols):
        logs.append(
            ASSIGN_NEW_MSG.format(
                new_cols=", ".join(columns_added(input_df, cols))
            )
        )
    logs = "\n".join(logs)
    return logs, tips


def log_query(output_df, input_df, expr, inplace=False, *args, **kwargs):
    logs, tips = get_filter_rows_logs(input_df, output_df)
    return logs, tips


def log_sort_index(
    output_df,
    input_df,
    axis=0,
    level=None,
    ascending=True,
    inplace=False,
    kind="quicksort",
    na_position="last",
    sort_remaining=True,
    by=None,
    **kwargs,
):
    logs = SORT_INDEX_MSG.format(ascending)
    tips = ""
    return logs, tips


def log_sort_values(
    output_df,
    input_df,
    by,
    axis=0,
    ascending=True,
    inplace=False,
    kind="quicksort",
    na_position="last",
    **kwargs,
):
    logs = SORT_VALUES_MSG.format(by, ascending)
    tips = ""
    return logs, tips


def log_tail(output_df, input_df, n=5, **kwargs):
    logs = TAIL_MSG.format(n)
    tips = SHOULD_REDUCED_ROW_TIP if is_same_rows(input_df, output_df) else ""
    return logs, tips


def log_head(output_df, input_df, n=5, **kwargs):
    logs = HEAD_MSG.format(n)
    tips = SHOULD_REDUCED_ROW_TIP if is_same_rows(input_df, output_df) else ""
    return logs, tips


def log_merge(
    output_df,
    input_df,
    right,
    how="inner",
    on=None,
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=False,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
    **kwargs,
):
    logs = []
    tips = ""
    merged = input_df.original_merge(
        right,
        "outer",
        on,
        left_on,
        right_on,
        left_index,
        right_index,
        sort,
        suffixes,
        copy,
        True,
        validate,
    )
    logs.append(
        JOIN_TYPE_MSG.format(how=how, **merged._merge.value_counts().to_dict())
    )
    if is_same_rows(input_df, output_df):
        logs.append(REMOVED_NO_ROWS_MSG)
    else:
        logs.append(JOIN_ROWS_MSG.format(output_rows=len(output_df)))
    if not is_same_cols(input_df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(input_df, output_df),
                new_columns=str_new_columns(input_df, output_df),
            )
        )

    logs = "\n".join(logs)
    return logs, tips


def log_join(
    output_df,
    input_df,
    other,
    on=None,
    how="left",
    lsuffix="",
    rsuffix="",
    sort=False,
    **kwargs,
):
    logs = []
    tips = ""
    merged = input_df.original_merge(
        other, "outer", on, input_df.index, other.index, indicator=True
    )
    logs.append(
        JOIN_TYPE_MSG.format(how=how, **merged._merge.value_counts().to_dict())
    )

    logs.append(get_filter_rows_logs(input_df, output_df))
    if not is_same_cols(input_df, output_df):
        logs.append(
            JOIN_NEW_COLS_MSG.format(
                num_new_columns=num_new_columns(input_df, output_df),
                new_columns=str_new_columns(input_df, output_df),
            )
        )
    logs = "\n".join(logs)
    return logs, tips


def log_fillna(
    output_df,
    input_df,
    value=None,
    method=None,
    axis=None,
    inplace=False,
    limit=None,
    downcast=None,
    **kwargs,
):
    tips = ""
    value = "empty string" if value == "" else value
    if num_of_na(input_df) == num_of_na(output_df):
        logs = FILLNA_NO_NA_MSG
        tips = FILLNA_NO_NA_TIP
    else:
        logs = FILLNA_WITHH_NA_MSG.format(num_of_na(input_df), value)
    return logs, tips


def log_sample(
    output_df,
    input_df,
    n=None,
    frac=None,
    replace=False,
    weights=None,
    random_state=None,
    axis=None,
    *args,
    **kwargs,
):
    logs = SAMPLE_MSG.format(output_rows=len(output_df))
    tips = SHOULD_REDUCED_ROW_TIP if is_same_rows(input_df, output_df) else ""
    return logs, tips


def log_nlargest(output_df, input_df, n, columns, keep="first", **kwargs):
    # todo maybe wrong
    logs = NLARGEST_MSG.format(n=n, cols=columns)
    tips = SHOULD_REDUCED_ROW_TIP if is_same_rows(input_df, output_df) else ""
    return logs, tips


def log_nsmallest(output_df, input_df, n, columns, keep="first", **kwargs):
    logs = NSMALLEST_MSG.format(n=n, cols=columns)
    tips = SHOULD_REDUCED_ROW_TIP if is_same_rows(input_df, output_df) else ""
    return logs, tips


def log_groupby(
    output_df,
    input_df,
    by=None,
    axis=0,
    level=None,
    as_index=True,
    sort=True,
    group_keys=True,
    squeeze=False,
    observed=False,
    **kwargs,
):
    tips = []
    group_by = ", ".join(by)
    groups = list(output_df.groups)
    groups_len = len(groups)
    groups_repr = (
        ", ".join(groups)
        if groups_len < 5
        else ", ".join(groups[:5]) + " and more"
    )
    tips = ""
    logs = GROUPBY_MSG.format(group_by, groups_len, groups_repr)
    return logs, tips


def log__iterrows(output_df, input_df):
    tips = ITERROWS_TIPS
    logs = ""
    return logs, tips


def log___getitem__(output_df, input_df, key, *args, **kwargs):
    logs = []
    tips = ""

    if isinstance(key, str):
        # Naive handle of __getitem__ which return series
        logs = TRANSFORMED_TO_DF_MSG
        return logs, tips

    if not is_same_cols(input_df, output_df):
        logs.append(
            FILTERED_COLS_MSG.format(
                cols_removed=cols_removed(input_df, output_df),
                cols_remaining=cols_remaining(output_df),
            )
        )
    if not is_same_rows(input_df, output_df):
        logs.append(
            FILTERED_ROWS_MSG.format(
                rows_removed=rows_removed(input_df, output_df),
                rows_removed_pct=rows_removed_pct(input_df, output_df),
                rows_remaining=rows_remaining(output_df),
            )
        )
    logs = "\n".join(logs)
    return logs, tips


# TODO add tip on types+cardinality

if __name__ == "__main__":
    pass
