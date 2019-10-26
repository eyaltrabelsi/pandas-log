
Usage
=====

For a cleaner use-case I would `go here
<https://towardsdatascience.com/introducing-pandas-log-3240a5e57e21>`_

First we need to load some libraries including pandas-log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    import pandas as pd
    import numpy as np
    import pandas_log

Let’s take a look at our dataset:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    df = pd.read_csv("pokemon.csv")
    df.head(10)




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
          <th>legendary</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>1</td>
          <td>Bulbasaur</td>
          <td>Grass</td>
          <td>Poison</td>
          <td>318</td>
          <td>45</td>
          <td>49</td>
          <td>49</td>
          <td>65</td>
          <td>65</td>
          <td>45</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>1</th>
          <td>2</td>
          <td>Ivysaur</td>
          <td>Grass</td>
          <td>Poison</td>
          <td>405</td>
          <td>60</td>
          <td>62</td>
          <td>63</td>
          <td>80</td>
          <td>80</td>
          <td>60</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>2</th>
          <td>3</td>
          <td>Venusaur</td>
          <td>Grass</td>
          <td>Poison</td>
          <td>525</td>
          <td>80</td>
          <td>82</td>
          <td>83</td>
          <td>100</td>
          <td>100</td>
          <td>80</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>3</th>
          <td>3</td>
          <td>VenusaurMega Venusaur</td>
          <td>Grass</td>
          <td>Poison</td>
          <td>625</td>
          <td>80</td>
          <td>100</td>
          <td>123</td>
          <td>122</td>
          <td>120</td>
          <td>80</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>4</th>
          <td>4</td>
          <td>Charmander</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>309</td>
          <td>39</td>
          <td>52</td>
          <td>43</td>
          <td>60</td>
          <td>50</td>
          <td>65</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>5</th>
          <td>5</td>
          <td>Charmeleon</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>405</td>
          <td>58</td>
          <td>64</td>
          <td>58</td>
          <td>80</td>
          <td>65</td>
          <td>80</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>6</th>
          <td>6</td>
          <td>Charizard</td>
          <td>Fire</td>
          <td>Flying</td>
          <td>534</td>
          <td>78</td>
          <td>84</td>
          <td>78</td>
          <td>109</td>
          <td>85</td>
          <td>100</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>7</th>
          <td>6</td>
          <td>CharizardMega Charizard X</td>
          <td>Fire</td>
          <td>Dragon</td>
          <td>634</td>
          <td>78</td>
          <td>130</td>
          <td>111</td>
          <td>130</td>
          <td>85</td>
          <td>100</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>8</th>
          <td>6</td>
          <td>CharizardMega Charizard Y</td>
          <td>Fire</td>
          <td>Flying</td>
          <td>634</td>
          <td>78</td>
          <td>104</td>
          <td>78</td>
          <td>159</td>
          <td>115</td>
          <td>100</td>
          <td>1</td>
          <td>False</td>
        </tr>
        <tr>
          <th>9</th>
          <td>7</td>
          <td>Squirtle</td>
          <td>Water</td>
          <td>NaN</td>
          <td>314</td>
          <td>44</td>
          <td>48</td>
          <td>65</td>
          <td>50</td>
          <td>64</td>
          <td>43</td>
          <td>1</td>
          <td>False</td>
        </tr>
      </tbody>
    </table>
    </div>



Lets say we want to find out:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Who is the weakest non-legendary fire pokemon?
----------------------------------------------



The strategy will probably be something like:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Filter out legendary pokemons using ``.query()`` .
2. Keep only fire pokemons using ``.query()`` .
3. Drop Legendary column using ``.drop()`` .
4. Keep the weakest pokemon among them using ``.nsmallest()`` .
5. Reset index using ``.reset_index()`` .

.. code:: ipython3

    res = (df.copy()
             .query("legendary==0")
             .query("type_1=='fire' or type_2=='fire'")
             .drop("legendary", axis=1)
             .nsmallest(1,"total")
             .reset_index(drop=True)
          )
    res




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



OH NOO!!! Our code does not work !! We got no records
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



If only there was a way to track those issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fortunetly thats what **pandas-log** is for! either as a global function
or context manager. This the example with pandas_log’s
``context_manager``.

.. code:: ipython3

    with pandas_log.enable():
        res = (df.query("legendary==0")
                 .query("type_1=='fire' or type_2=='fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
              )
    res


.. parsed-literal::


    1) [1mquery[0m(expr="legendary==0", inplace=False):
    	[4mMetadata[0m:
    	* Removed 65 rows (8.125%), 735 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 199.4 kB.
    	* Output Dataframe size is 188.5 kB.

    2) [1mquery[0m(expr="type_1=='fire' or type_2=='fire'", inplace=False):
    	[4mMetadata[0m:
    	* Removed 735 rows (100.0%), 0 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 188.5 kB.
    	* Output Dataframe size is 0 Bytes.

    3) [1mdrop[0m(labels="legendary", axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
    	[4mMetadata[0m:
    	* Removed the following columns (legendary) now only have the following columns (attack, sp_def, speed, hp, total, type_2, #, name, type_1, generation, defense, sp_atk).
    	* No change in number of rows of input df.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 0 Bytes.
    	* Output Dataframe size is 0 Bytes.

    4) [1mnsmallest[0m(n=1, columns="total", keep='first'):
    	[4mMetadata[0m:
    	* Picked 1 smallest rows by columns (total).
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 0 Bytes.
    	* Output Dataframe size is 0 Bytes.




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
      </tbody>
    </table>
    </div>



We can see clearly that in the second step (``.query()``) we filter all the rows!! and indeed we should of writen Fire as oppose to fire
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    res = (df.copy()
             .query("type_1=='Fire' or type_2=='Fire'")
             .query("legendary==0")
             .drop("legendary", axis=1)
             .nsmallest(1,"total")
             .reset_index(drop=True)
          )
    res




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>218</td>
          <td>Slugma</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>250</td>
          <td>40</td>
          <td>40</td>
          <td>40</td>
          <td>70</td>
          <td>40</td>
          <td>20</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>



Whoala we got Slugma !!!!!!!!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Some more advance usage
-----------------------

One can use verbose variable which allows lower level logs functionalities like whether the dataframe was copied as part of pipeline.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This can explain comparision issues.

.. code:: ipython3

    with pandas_log.enable(verbose=True):
        res = (df.query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mquery[0m(expr="legendary==0", inplace=False):
    	[4mMetadata[0m:
    	* Removed 65 rows (8.125%), 735 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 199.4 kB.
    	* Output Dataframe size is 188.5 kB.

    2) [1mquery[0m(expr="type_1=='Fire' or type_2=='Fire'", inplace=False):
    	[4mMetadata[0m:
    	* Removed 679 rows (92.38095238095238%), 56 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 188.5 kB.
    	* Output Dataframe size is 14.4 kB.

    3) [1mdrop[0m(labels="legendary", axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
    	[4mMetadata[0m:
    	* Removed the following columns (legendary) now only have the following columns (attack, sp_def, speed, hp, total, type_2, #, name, type_1, generation, defense, sp_atk).
    	* No change in number of rows of input df.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.4 kB.
    	* Output Dataframe size is 14.3 kB.

    X) [1m__getitem__[0m(key="total"):
    	Metadata:

    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.3 kB.
    	* Output Dataframe size is 896 Bytes.

    X) [1mcopy[0m(deep=True):
    	[4mMetadata[0m:
    	* Using default strategy (some metric might not be relevant).
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.3 kB.
    	* Output Dataframe size is 14.3 kB.

    X) [1mreset_index[0m(level=None, drop=False, inplace=False, col_level=0, col_fill=''):
    	Metadata:

    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.3 kB.
    	* Output Dataframe size is 14.0 kB.

    X) [1m__getitem__[0m(key="total"):
    	Metadata:

    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.0 kB.
    	* Output Dataframe size is 576 Bytes.

    4) [1mnsmallest[0m(n=1, columns="total", keep='first'):
    	[4mMetadata[0m:
    	* Picked 1 smallest rows by columns (total).
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.3 kB.
    	* Output Dataframe size is 236 Bytes.

    X) [1mcopy[0m(deep=True):
    	[4mMetadata[0m:
    	* Using default strategy (some metric might not be relevant).
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 236 Bytes.
    	* Output Dataframe size is 236 Bytes.

    X) [1mreset_index[0m(level=None, drop=False, inplace=False, col_level=0, col_fill=''):
    	Metadata:

    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 236 Bytes.
    	* Output Dataframe size is 356 Bytes.




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>218</td>
          <td>Slugma</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>250</td>
          <td>40</td>
          <td>40</td>
          <td>40</td>
          <td>70</td>
          <td>40</td>
          <td>20</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>



as we can see after both the drop and nsmallest functions the dataframe
was being copied

One can use silent variable which allows to suppress stdout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    with pandas_log.enable(silent=True):
        res = (df.copy()
                 .query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>218</td>
          <td>Slugma</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>250</td>
          <td>40</td>
          <td>40</td>
          <td>40</td>
          <td>70</td>
          <td>40</td>
          <td>20</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>



One can use full_signature variable which allows to suppress the signature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    with pandas_log.enable(full_signature=False):
        res = (df.query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mquery[0m(expr="legendary==0", inplace=False):
    	[4mMetadata[0m:
    	* Removed 65 rows (8.125%), 735 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 199.4 kB.
    	* Output Dataframe size is 188.5 kB.

    2) [1mquery[0m(expr="type_1=='Fire' or type_2=='Fire'"):
    	[4mMetadata[0m:
    	* Removed 679 rows (92.38095238095238%), 56 rows remaining.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 188.5 kB.
    	* Output Dataframe size is 14.4 kB.

    3) [1mdrop[0m(labels="legendary"):
    	[4mMetadata[0m:
    	* Removed the following columns (legendary) now only have the following columns (attack, sp_def, speed, hp, total, type_2, #, name, type_1, generation, defense, sp_atk).
    	* No change in number of rows of input df.
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.4 kB.
    	* Output Dataframe size is 14.3 kB.

    4) [1mnsmallest[0m(n=1, columns="total"):
    	[4mMetadata[0m:
    	* Picked 1 smallest rows by columns (total).
    	[4mExecution Stats[0m:
    	* Execution time: Step Took a moment seconds..
    	* Input Dataframe size is 14.3 kB.
    	* Output Dataframe size is 236 Bytes.




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>#</th>
          <th>name</th>
          <th>type_1</th>
          <th>type_2</th>
          <th>total</th>
          <th>hp</th>
          <th>attack</th>
          <th>defense</th>
          <th>sp_atk</th>
          <th>sp_def</th>
          <th>speed</th>
          <th>generation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>218</td>
          <td>Slugma</td>
          <td>Fire</td>
          <td>NaN</td>
          <td>250</td>
          <td>40</td>
          <td>40</td>
          <td>40</td>
          <td>70</td>
          <td>40</td>
          <td>20</td>
          <td>2</td>
        </tr>
      </tbody>
    </table>
    </div>


