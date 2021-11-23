# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ## Topics in Pandas
# **Stats 507, Fall 2021** 
#   
#
# ## Contents
# Add a bullet for each topic and link to the level 2 title header using 
# the exact title with spaces replaced by a dash. 
#
# + [Empty cells](#Empty-cells)
# + [Windows Rolling](#Windows-Rolling) 
# + [Data Transformation](#Data-Transformation)


# ## Empty cells
# ---
# **Name: Yan Xu**
#
# Email:yanyanxu@umich.edu

import pandas as pd
import numpy as np
from datetime import datetime
from ps1_solution import ci_prop
import numpy.random as npra
from warnings import warn
import matplotlib.pyplot as plt
from os.path import exists


from scipy import stats
from scipy.stats import chi2_contingency 
from IPython.display import HTML

# Remove rows: remove rows that contain empty cells. Since data sets can be very big, and removing a few rows will not have a big impact on the result.
# Replace Empty Values:insert a new value using fillna() to replace NA.
# Replace Only For a Specified Columns: To only replace empty values for one column, specify the column name for the DataFrame.

#If you want to consider inf and -inf to be “NA” in computations
pd.options.mode.use_inf_as_na = True

df = pd.read_csv('https://www.w3schools.com/python/pandas/dirtydata.csv.txt')
df #The dataframe containing bad data we want to clean

# To make detecting missing values easier (and across different array dtypes), pandas provides the isna() and notna() functions, which are also methods on Series and DataFrame objects

df["Date"][20:25].notna()

new_df = df.dropna()
print(new_df.to_string())#dropna() method returns a new DataFrame, and will not change the original.
#If you want to change the original DataFrame, use the `inplace = True` argument

#insert a new value to replace the empty values
df.fillna(130)
df["Calories"].fillna(130, inplace = True)#only replace empty values for one column


# ### Data in wrong format
# 
# In our Data Frame, we have two cells with the wrong format.
# Check out row 22 and 26, the 'Date' column should be a string that represents a date,try to convert all cells in the 'Date' column into dates.

# Method to validate a date string format in Python


date_string = '12-25-2018'
format = "%Y/%m/d"

try:
  datetime.strptime(date_string, format)
  print("This is the correct date string format.")
except ValueError:
  print("This is the incorrect date string format. It should be YYYY/MM/DD")


# This is the incorrect date string format. It should be YYYY/MM/DD

# for row 26,the "date" column is in wrong format
df['Date'] = pd.to_datetime(df['Date'])


# ### Removing Duplicates
# 
# Duplicate rows are rows that have been registered more than one time.
# To discover duplicates, we can use the duplicated() method.
# The duplicated() method returns a Boolean values for each row.

print(df[10:15].duplicated())


# To remove duplicates, use the drop_duplicates() method.

df.drop_duplicates(inplace = True)  


# ## Windows Rolling
# ---
# **Name: Junyuan Yang**
#
# **UM email: junyyang@umich.edu**
#
# Return a rolling object allowing summary functions to be applied to windows of length n.
# By default, the result is set to the right edge of the window. This can be changed to the center of the window by setting center=True.
# Each points' weights could be determined by win_type shown in windows function, or evenly weighted as default.

import numpy as np
import pandas as pd
from os.path import exists
import re

rng = np.random.default_rng(9 * 2021 * 28)
n=100
a = rng.binomial(n=1, p=0.5, size=n)
b = 1 - 0.5 * a + rng.normal(size=n)
c = 0.8 * a + rng.normal(size=n) 
df = pd.DataFrame({'a': a, 'b': b, 'c': c})
df['c'].plot()

# - Calculating the mean in centered windows with a window length of 10 and windows type of 'triangular'

df['c'].rolling(10, center=True, win_type='triang').mean().plot()

# - Except existing functions like `sum`, `mean` and `std`, you could also use the self defined funciton by `agg.()`

df['c'].rolling(10).agg(lambda x: max(x)).plot()


# ## Data Transformation 
# ---
# **Name: Tong Wu**
#
# **UM email: wutongg@umich.edu**  
#
# Data transforming technique is important and useful when we prepare the data
# for analysis.  
# - Removing duplicates
# - Replacing values
# - Discretization and binning
# - Detecting and filtering outliers
# - Computing indicator/dummy variables
# ### Removing duplicates
# - Use `duplicated()` method returning a boolean Series to indicate which row
# is duplicated or not.
# - Duplicated rows will be dropped using `drop_duplicates()` when the
# duplicated arrary is `False`.

import pandas as pd
import numpy as np
import scipy.stats as st

data = pd.DataFrame({
    'a': [('red', 'black')[i % 2] for i in range(7)],
    'b': [('x', 'y', 'z')[i % 3] for i in range(7)]
    })
data.duplicated()
data.drop_duplicates()

# - We can specify a subset of data to detect duplicates.

data.drop_duplicates(['a'])

# - Above methods by default keep the first observed duplicated, but we can 
# keep the last occurance and drop the first occurance.

data.drop_duplicates(['a', 'b'], keep='last')

# ### Replacing values
# - General replacing approach
#  + When we find flag values for missing value, we can replace them with NAs.

pd.Series([1., -999., 2., -999., 5., 3.]).replace(-999, np.nan)

# - In a special case, we need to detect missing values and fill in them. 
#  +  Built-in Python `None` value is also treated as `NA`.

data1 = pd.DataFrame(np.random.randn(6,3))
data1.iloc[:3, 1] = np.nan
data1.iloc[:2, 2] = np.nan
data1.iloc[1, 0] = None

# Detect missing values by rows and drop rows with all NAs.
data1.dropna(axis=0, how='all')
# For time seris data, we want to keep rows with obervations.
data1.dropna(thresh=2)

# Fill in missing values.
# - Note that `fillna()` method return a new object by default.
#  + Using `inplace=True` to modify the existing object.
# - `ffill` method propagate last valid observation forward.

data1.fillna(0)
_ = data1.fillna(method='ffill', inplace=True)

# ### Discretization and binning
# This technique is used when we want to analyze continuous data seperated
# into different bins.  
# For example, we have a group of people and the **age** isgrouped into bins.

ages = [20, 17, 25, 27, 21, 23, 37, 31, 61, 45, 41, 88]
# Default it is cut into intervals with left side opened and right side closed
bins = [15, 25, 35, 60, 90]
cats = pd.cut(ages, bins)
# Categorical object
cats
cats.codes
cats.categories
# Bins count
pd.value_counts(cats)

# - Cut without emplicit bin edges.
#  + It will compute equal-length bins using the range of data.

pd.cut(ages, 4, precision=2)

# - Cut data based on sample quantiles
cat2 = pd.qcut(np.random.randn(1000), 4, precision=2)
pd.value_counts(cat2)


# ### Detecting and filtering outliers
# Here is an example with normal distributed data.
data2 = pd.DataFrame(np.random.randn(1000, 4))
data2.describe()

# Find rows which contains absolute value is larger than 3.
data2[(np.abs(data2) > 3).any(1)]
# Cap values outside the interval -3 to 3
data2[(np.abs(data2) > 3)] = np.sign(data2) * 3
data2.describe()

# ### Computing indicator/dummy variables
# We can convert a categorical variable into an indicator matrix. That is if
# a column contains $k$ distinct values, the indicator matrix is derived with
# $k$ colunms with 1s and 0s.

pd.get_dummies(cats)
