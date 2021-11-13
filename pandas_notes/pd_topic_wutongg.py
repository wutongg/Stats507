# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Problem Set 4, Question 0
# **Tong Wu**
# **Email: wutongg@umich.edu**  
# *October 20, 2021*

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem set 4 

@author: Tong Wu
@date: October 20, 2021
"""

# # Question 0 - Data Transformation
# ## Overview  
# Data transforming technique is important and useful when we prepare the data
# for analysis.  
# - Removing duplicates
# - Replacing values
# - Discretization and binning
# - Detecting and filtering outliers
# - Computing indicator/dummy variables
# ## Removing duplicates
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

# ## Replacing values
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

# ## Discretization and binning
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


# ## Detecting and filtering outliers
# Here is an example with normal distributed data.
data2 = pd.DataFrame(np.random.randn(1000, 4))
data2.describe()

# Find rows which contains absolute value is larger than 3.
data2[(np.abs(data2) > 3).any(1)]
# Cap values outside the interval -3 to 3
data2[(np.abs(data2) > 3)] = np.sign(data2) * 3
data2.describe()

# ## Computing indicator/dummy variables
# We can convert a categorical variable into an indicator matrix. That is if
# a column contains $k$ distinct values, the indicator matrix is derived with
# $k$ colunms with 1s and 0s.

pd.get_dummies(cats)
