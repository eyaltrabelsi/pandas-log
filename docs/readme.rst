===============
Why pandas-log?
===============

``Pandas-log`` is a Python implementation of the R package ``tidylog``, and provides a feedback about basic pandas operations.

The pandas has been invaluable for the data science ecosystem and usually consists of a series of steps that involve transforming raw data into an understandable/usable format.
These series of steps need to be run in a certain sequence and if the result is unexpected it's hard to understand what happened.
``Pandas-log`` log metadata on each operation which will allow to pinpoint the issues like:

    - Wrong predicate expressions.
    - Copying of our DataFrames.
    - Wrong joins/merge.
    - Performance Issues.
    - More

For medium article `go here
<https://towardsdatascience.com/introducing-pandas-log-3240a5e57e21>`_

For a full walkthrough `go here
<https://github.com/eyaltrabelsi/pandas-log/blob/master/examples/pandas_log_intro.ipynb>`_
