=====
Usage
=====


First we need to load some libraries including pandas-log
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

    import pandas as pd
    import numpy as np
    import pandas_log

Let’s take a look at our dataset:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code::

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

.. code::

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

.. code::

    with pandas_log.enable():
        res = (df.copy()
                 .query("legendary==0")
                 .query("type_1=='fire' or type_2=='fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mquery[0m(expr="legendary==0", inplace=False):
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    	* Step Took 0.0025560855865478516 seconds

    2) [1mquery[0m(expr="type_1=='fire' or type_2=='fire'", inplace=False):
    	* Removed 735 rows (1.0%), 0 rows remaining.
    	* Step Took 0.0040740966796875 seconds

    3) [1mdrop[0m(labels="legendary", axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
    	* Removed the following columns (legendary) now only have the following columns (sp_def,defense,generation,speed,name,type_2,hp,sp_atk,type_1,#,total,attack).
    	* No change in number of rows.
    	* Step Took 0.0007641315460205078 seconds

    4) [1mnsmallest[0m(n=1, columns="total", keep='first'):
    	* Picked 1 smallest rows by columns (total).
    	* Step Took 0.0023779869079589844 seconds




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

.. code::

    pandas_log.auto_enable()
    res = (df.copy()
             .query("legendary==0")
             .query("type_1=='fire' or type_2=='fire'")
             .drop("legendary", axis=1)
             .nsmallest(1,"total")
             .reset_index(drop=True)
          )
    pandas_log.auto_disable()
    res


.. parsed-literal::


    1) [1mquery[0m(expr="legendary==0", inplace=False):
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    	* Step Took 0.0027070045471191406 seconds

    2) [1mquery[0m(expr="type_1=='fire' or type_2=='fire'", inplace=False):
    	* Removed 735 rows (1.0%), 0 rows remaining.
    	* Step Took 0.0044138431549072266 seconds

    3) [1mdrop[0m(labels="legendary", axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
    	* Removed the following columns (legendary) now only have the following columns (sp_def,defense,generation,speed,name,type_2,hp,sp_atk,type_1,#,total,attack).
    	* No change in number of rows.
    	* Step Took 0.0010120868682861328 seconds

    4) [1mnsmallest[0m(n=1, columns="total", keep='first'):
    	* Picked 1 smallest rows by columns (total).
    	* Step Took 0.0033338069915771484 seconds




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

.. code::


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

.. code::

    with pandas_log.enable(verbose=True):
        res = (df.copy()
                 .query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mcopy[0m(deep=True):
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.0005130767822265625 seconds

    2) [1mquery[0m(expr="legendary==0", inplace=False):
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    	* Step Took 0.0033111572265625 seconds

    3) [1mquery[0m(expr="type_1=='Fire' or type_2=='Fire'", inplace=False):
    	* Removed 679 rows (0.9238095238095239%), 56 rows remaining.
    	* Step Took 0.003696918487548828 seconds

    4) [1mdrop[0m(labels="legendary", axis=0, index=None, columns=None, level=None, inplace=False, errors='raise'):
    	* Removed the following columns (legendary) now only have the following columns (sp_def,defense,generation,speed,name,type_2,hp,sp_atk,type_1,#,total,attack).
    	* No change in number of rows.
    	* Step Took 0.0008273124694824219 seconds

    5) [1mcopy[0m(deep=True):
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.00017905235290527344 seconds

    5) [1mnsmallest[0m(n=1, columns="total", keep='first'):
    	* Picked 1 smallest rows by columns (total).
    	* Step Took 0.0014688968658447266 seconds

    6) [1mcopy[0m(deep=True):
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.0001900196075439453 seconds




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

.. code::

    with pandas_log.enable(silent=True):
        res = (df.copy()
                 .query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mcopy[0m(deep=True):
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.00025963783264160156 seconds




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

.. code::

    with pandas_log.enable(full_signature=False):
        res = (df.copy()
                 .query("legendary==0")
                 .query("type_1=='Fire' or type_2=='Fire'")
                 .drop("legendary", axis=1)
                 .nsmallest(1,"total")
                 .reset_index(drop=True)
              )
    res


.. parsed-literal::


    1) [1mcopy[0m(deep=True):
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.0002608299255371094 seconds

    2) [1mquery[0m(expr="legendary==0"):
    	* Removed 65 rows (0.08125%), 735 rows remaining.
    	* Step Took 0.002346038818359375 seconds

    3) [1mquery[0m(expr="type_1=='Fire' or type_2=='Fire'"):
    	* Removed 679 rows (0.9238095238095239%), 56 rows remaining.
    	* Step Took 0.0029571056365966797 seconds

    4) [1mdrop[0m(labels="legendary"):
    	* Removed the following columns (legendary) now only have the following columns (sp_def,defense,generation,speed,name,type_2,hp,sp_atk,type_1,#,total,attack).
    	* No change in number of rows.
    	* Step Took 0.0006778240203857422 seconds

    5) [1mcopy[0m():
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.00016117095947265625 seconds

    5) [1mnsmallest[0m(n=1, columns="total"):
    	* Picked 1 smallest rows by columns (total).
    	* Step Took 0.0014069080352783203 seconds

    6) [1mcopy[0m():
    	* using default strategy (some metric might not be relevant)
    	* Step Took 0.0001609325408935547 seconds




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


