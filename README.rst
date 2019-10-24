==========
pandas-log
==========


.. image:: https://img.shields.io/pypi/v/pandas_log.svg
        :target: https://pypi.python.org/pypi/pandas_log

.. image:: https://img.shields.io/travis/eyaltrabelsi/pandas-log.svg
        :target: https://travis-ci.org/eyaltrabelsi/pandas-log

.. image:: https://readthedocs.org/projects/pandas-log/badge/?version=latest
        :target: https://pandas-log.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/eyaltrabelsi/pandas-log/shield.svg
     :target: https://pyup.io/repos/github/eyaltrabelsi/pandas-log/
     :alt: Updates

The goal of pandas-log is to provide feedback about basic pandas operations. It provides simple wrapper functions for the most common functions, such as ``.query``, ``.apply``, ``.merge``, ``.group_by`` and more.

Why pandas-log?
---------------
``Pandas-log`` is a Python implementation of the R package ``tidylog``, and provides a feedback about basic pandas operations.

The pandas has been invaluable for the data science ecosystem and usually consists of a series of steps that involve transforming raw data into an understandable/usable format.
These series of steps need to be run in a certain sequence and if the result is unexpected it's hard to understand what happened. ``Pandas-log`` log metadata on each operation which will allow to pinpoint the issues.



Lets look at an example, first we need to load ``pandas-log`` after ``pandas`` and create a dataframe:

.. code-block:: python

    import pandas
    import pandas_logs

    with pandas_logs.enable():
        df = pd.DataFrame({"name": ['Alfred', 'Batman', 'Catwoman'],
                       "toy": [np.nan, 'Batmobile', 'Bullwhip'],
                       "born": [pd.NaT, pd.Timestamp("1940-04-25"), pd.NaT]})


``pandas-log`` will give you feedback, for instance when filtering a data frame or adding a new variable:

.. code-block:: python

    df.assign(toy=lambda x: x.toy.map(str.lower))
      .query("name != 'Batman'")

``pandas-log`` can be especially helpful in longer pipes:

.. code-block:: python

    df.assign(toy=lambda x: x.toy.map(str.lower))
      .query("name != 'Batman'")
      .dropna()\
      .assign(lower_name=lambda x: x.name.map(str.lower))
      .reset_index()

For medium article `go here
<https://towardsdatascience.com/introducing-pandas-log-3240a5e57e21>`_

For a full walkthrough `go here
<https://github.com/eyaltrabelsi/pandas-log/blob/master/examples/pandas_log_intro.ipynb>`_


Installation
------------
``pandas-log`` is currently installable from PyPI:

.. code-block:: bash

    pip install pandas-log


Contributing
------------
Follow `contribution docs
<https://pandas-log.readthedocs.io/en/latest/contributing.html>`_ for a full description of the process of contributing to ``pandas-log``.
