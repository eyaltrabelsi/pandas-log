=====
Usage
=====


Why pandas-log?
---------------

Pandas-log is a Python implementation of the R package tidylog, and
provides a feedback about basic pandas operations.

The pandas has been invaluable for the data science ecosystem and
usually consists of a series of steps that involve transforming raw data
into an understandable/usable format. These series of steps need to be
run in a certain sequence and if the result is unexpected it’s hard to
understand what happened. Pandas-log log metadata on each operation
which will allow to pinpoint the issues.

Pandas-log Demo
---------------

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

    res = (df.query("legendary==0")
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
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::

    1) query(self="legendary==0"):
    	* Step Took 0.0024781227111816406 seconds
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    2) query(self="type_1=='fire' or type_2=='fire'"):
    	* Step Took 0.0037260055541992188 seconds
    	* Removed 735 rows (1.0%), 0 rows remaining.
    3) reindex():
    	* Step Took 0.0005040168762207031 seconds
    3) drop(self="legendary"):
    	* Step Took 0.0009241104125976562 seconds
    	* Removed the following columns (legendary) now only have the following columns (hp,type_2,defense,#,speed,type_1,generation,sp_def,attack,name,sp_atk,total).
    	* No change in number of rows.
    4) reset_index():
    	* Step Took 0.00023794174194335938 seconds
    4) nsmallest(self="1",n="total"):
    	* Step Took 0.0027031898498535156 seconds
    	* Picked 1 smallest rows by columns (total).
    5) reset_index():
    	* Step Took 0.00019979476928710938 seconds




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



This the example with pandas_log’s ``auto_enable``

.. code:: ipython3

    pandas_log.auto_enable()
    res = (df.query("legendary==0")
             .query("type_1=='fire' or type_2=='fire'")
             .drop("legendary", axis=1)
             .nsmallest(1,"total")
             .reset_index(drop=True)
          )
    pandas_log.auto_disable()
    res


.. parsed-literal::

    1) query(self="legendary==0"):
    	* Step Took 0.002357006072998047 seconds
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    2) query(self="type_1=='fire' or type_2=='fire'"):
    	* Step Took 0.0037169456481933594 seconds
    	* Removed 735 rows (1.0%), 0 rows remaining.
    3) reindex():
    	* Step Took 0.0008518695831298828 seconds
    3) drop(self="legendary"):
    	* Step Took 0.001394033432006836 seconds
    	* Removed the following columns (legendary) now only have the following columns (hp,type_2,defense,#,speed,type_1,generation,sp_def,attack,name,sp_atk,total).
    	* No change in number of rows.
    4) reset_index():
    	* Step Took 0.00019311904907226562 seconds
    4) nsmallest(self="1",n="total"):
    	* Step Took 0.0024139881134033203 seconds
    	* Picked 1 smallest rows by columns (total).
    5) reset_index():
    	* Step Took 0.00020575523376464844 seconds




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


    res = (df.query("type_1=='Fire' or type_2=='Fire'")
             .query("legendary==0")
             .drop("legendary", axis=1)
             .nsmallest(1,"total")
             .reset_index(drop=True)
          )
    res


.. parsed-literal::

    1) query(self="type_1=='Fire' or type_2=='Fire'"):
    	* Step Took 0.0030159950256347656 seconds
    	* Removed 736 rows (0.92%), 64 rows remaining.




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

    1) query(self="legendary==0"):
    	* Step Took 0.0025539398193359375 seconds
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    2) query(self="type_1=='Fire' or type_2=='Fire'"):
    	* Step Took 0.0038051605224609375 seconds
    	* Removed 679 rows (0.9238095238095239%), 56 rows remaining.
    3) reindex():
    	* Step Took 0.0004749298095703125 seconds
    3) drop(self="legendary"):
    	* Step Took 0.0007948875427246094 seconds
    	* Removed the following columns (legendary) now only have the following columns (hp,type_2,defense,#,speed,type_1,generation,sp_def,attack,name,sp_atk,total).
    	* No change in number of rows.
    4) copy():
    	* Step Took 0.00015687942504882812 seconds
    4) reset_index():
    	* Step Took 0.00031185150146484375 seconds
    4) nsmallest(self="1",n="total"):
    	* Step Took 0.0015668869018554688 seconds
    	* Picked 1 smallest rows by columns (total).
    5) copy():
    	* Step Took 0.0003211498260498047 seconds
    5) reset_index():
    	* Step Took 0.0006539821624755859 seconds




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
        res = (df.query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::

    1) query(self="legendary==0"):
    	* Step Took 0.002171754837036133 seconds
    	* Removed 65 rows (0.08125%), 735 rows remaining.




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


