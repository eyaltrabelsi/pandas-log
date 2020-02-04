import pandas as pd
import pandas_flavor as pf
from pandas_log.pandas_log import disable

@pf.register_dataframe_method
def dq_check(df, percentiles=None, thorough=True):
    '''
    Expanded "data quality" check that uses pd.DataFrame.describe as a base. Reports pertinent metrics
    automatically depending on datatypes present.
    :param df: pd.DataFrame
    :param percentiles: list-like of numbers passed directly to the percentiles argument of df.describe. Should be
        between 0 and 1.
    :param thorough: bool, whether to compute the more computationally expensive metrics
    :return: pd.DataFrame of results, analogous to output of pd.DataFrame.describe
    '''
    with disable():
        # Start with the base description
        description = df.describe(percentiles=percentiles, include='all')
        # Make the names more informative (not all of these are necessarily present depending on datatypes)
        description = description.rename(index={
            'unique': 'n_unique',
            'top': 'mode',
            'freq': 'mode_freq',
            'first': 'dt_min',
            'last': 'dt_max'
        })
        # Calculate frequency of modal value, first calculating the modal value if we don't already have it
        mode = description.loc['mode'] if 'mode' in description.index else df.mode().iloc[0]
        # TODO: Possibly faster to just calculate description.value_counts()?
        mode_freq = description.loc['mode_freq'] if 'mode_freq' in description.index else (df == mode).sum()
        # Calculate number and percentage of missing values as length of df - count (which is always output by description)
        missing = (len(df) - description.loc['count']).astype(float)
        p_missing = missing / len(df)
        # Pull out the numeric columns and calculate the number <= 0
        numerics = df.select_dtypes('number')
        n_less_zero = (numerics < 0).sum()
        n_zero = (numerics == 0).sum()
        # Add column indicating whether a column is entirely unique values (excluding missing)
        n_unique = description.loc['n_unique'] if 'n_unique' in description.index else description.nunique()
        is_unique = n_unique.astype(float) == len(df)
        # "key" meaning both unique and non-missing (ie in a SQL sense)
        is_key = is_unique & (missing == 0)
        # Add a row just of what dtype each column is
        dtype = df.dtypes
        dtype.name = 'dtype'
        # Calculate more computationally involved metrics if thorough flag is passed
        strings = df.select_dtypes('object')
        is_empty_string = (strings == '').sum()
        if thorough:
            try:
                from sklearn.neighbors import LocalOutlierFactor
                from numpy import percentile
                def local_outlier_scores(col):
                    # Calculate 90th percentile and max of local outlier factor (smaller indicates more of an inlier)
                    # Only do 1D outlier detection for now
                    clf = LocalOutlierFactor()  # Use all default params
                    clf.fit(df[col])
                    lof = clf.negative_outlier_factor_ * -1
                    lof_90 = percentile(lof, 90)
                    lof_max = max(lof)
                    return pd.Series({'lof_90': lof_90, 'lof_max': lof_max})
                thorough_df = numerics.apply(local_outlier_scores)
            except ImportError:
                thorough_df = pd.DataFrame([])
            # For string columns, calculate how many have leading or trailing whitespace
            edge_whitespace = strings.apply(lambda col: col.str.match(r'^\s+.*|.*\s+$', na=False).sum())
            edge_whitespace = pd.DataFrame([edge_whitespace], index=['has_edge_whitespace'])
            thorough_df = pd.concat([thorough_df, edge_whitespace], axis=1)
        else:
            thorough_df = pd.DataFrame([])
        # Concatenate all the results
        check = pd.concat([description, thorough_df, pd.DataFrame(
            [dtype, missing, p_missing, n_unique, is_unique, is_key, mode, mode_freq,
            n_zero, n_less_zero, is_empty_string],
            index=['dtype', 'n_missing', 'p_missing', 'n_unique', 'is_unique', 'is_key', 'mode', 'mode_freq',
                  'n_zero', 'n_less_zero', 'is_empty_string']
        )], sort=True)
        # Since we might be adding some rows that already existed, drop the duplicates
        # This isn't perfectly performant but it's a dataframe of like 10 rows so it won't be noticeable
        check = check.loc[~check.index.duplicated()]
        percentile_indices = [ix for ix in check.index if ix.endswith('%')]
        # Reorder the metrics in a way that's more intuitive
        check = check.reindex([
            'dtype',
            'count',
            'n_missing',
            'p_missing',
            'has_edge_whitespace',
            'is_empty_string',
            'n_zero',
            'n_less_zero',
            'n_unique',
            'is_unique',
            'is_key',
            'mean',
            'std',
            'mode',
            'mode_freq',
            'min'] + percentile_indices + [
            'max',
            'lof_90',
            'lof_max',
            'dt_min',
            'dt_max'
            # Reindex creates (empty) rows if they don't exist so we just reindex with the maximal possible set of indices
            # and then drop the entirely empty rows
        ]).dropna(how='all')
        return check