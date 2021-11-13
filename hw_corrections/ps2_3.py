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

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem set 2 - Question 3.

@author: Tong Wu
@date: September 24, 2021
"""

# ## Question 3 - Use Pandas to read, clean, and append several data files

# **a**. Use Python and Pandas to read and append the demographic datasets 
# keeping only columns containing the unique ids (SEQN), age (RIDAGEYR), race 
# and ethnicity (RIDRETH3), education (DMDEDUC2), and marital status 
# (DMDMARTL), along with the following variables related to the survey 
# weighting: (RIDSTATR, SDMVPSU, SDMVSTRA, WTMEC2YR, WTINT2YR). Add an 
# additional column identifying to which cohort each case belongs. Rename the 
# columns with literate variable names using all lower case and convert each 
# column to an appropriate type. Finally, save the resulting data frame to a 
# serialized “round-trip” format of your choosing (e.g. pickle, feather, or 
# parquet).

import pandas as pd
import re

# Import files from URL.
df1 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT')
df2 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT')
df3 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT')
df4 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT')

dic = {'2011-2012': df1, '2013-2014': df2, '2015-2016': df3, 
       '2017-2018': df4}

df_all = pd.DataFrame()
for k in dic.keys():
    # We need to select columns first since each cohort has different 
    # variables.
    x = dic[k][['SEQN', 'RIDAGEYR', 'RIDRETH3', 'DMDEDUC2', 'DMDMARTL', 
                     'RIDSTATR', 'SDMVPSU', 'SDMVSTRA', 'WTMEC2YR', 
                     'WTINT2YR']].copy()
    # We add one column for each dataframes for identifying cohorts.
    x.loc[:, 'year'] = k
    # Append data files by rows.
    df_all = pd.concat([df_all, x], axis=0, ignore_index=True).copy()

# We need to convert each column to an appropriate type.
# - Note that RIDRETH3, DMDEDUC2, DMDMARTL, RIDSTATR variables are categorical 
# data.

var = ['RIDRETH3', 'DMDEDUC2', 'DMDMARTL', 'RIDAGEYR', 'RIDSTATR', 'SEQN', 
       'SDMVPSU', 'SDMVSTRA']
for v in var:
    if v == 'RIDRETH3':
        df_all[v] = pd.Categorical(df_all[v].replace({1: 'Mexican American',
        2: 'Other Hispanic', 3: 'Non-Hispanic White', 4: 'Non-Hispanic Black',
        6: 'Non-Hispanic Asian', 7: 'Other Race - Including Multi-Racial'}))
    elif v == 'DMDEDUC2':
        df_all[v] = pd.Categorical(df_all[v].replace({1: 'Less than 9th grade'
        , 2: '9-11th grade (Includes 12th grade with no diploma)',
        3: 'High school graduate/GED or equivalent', 
        4: 'Some college or AA degree', 5: 'College graduate or above',
        7: 'Refused', 9: 'Don\'t Know'}))
    elif v == 'DMDMARTL':
        df_all[v] = pd.Categorical(df_all[v].replace({1: 'Married', 
        2: 'Widowed', 3: 'Divorced', 4: 'Separated', 5: 'Never married', 
        6: 'Living with partner', 77: 'Refused', 99: 'Don\'t Know'}))
    elif v == 'RIDSTATR':
        df_all[v] = pd.Categorical(df_all[v].replace({1: 'Interviewed only', 
        2: 'Both interviewed and MEC examined'}))
    else: 
        # Those variables are integers but stored in floats.
        df_all[v] = df_all[[v]].astype('int')

# # Correction
# Comment from GSI:
# - Q3: -2 for some names are too long.

# Rename the columns with literate variable names using all lower case.
df_all.rename(columns={'SEQN': 'id',
                       'RIDAGEYR': 'age',
                       'RIDRETH3': 'race',
                       'DMDEDUC2': 'education',
                       'DMDMARTL': 'marital status',
                       'RIDSTATR': 'exam status',
                       'SDMVPSU': 'psu',
                       'SDMVSTRA': 'strata',
                       'WTMEC2YR': 'exam wt',
                       'WTINT2YR': 'interview wt'}, inplace=True)                                                  

print(df_all.head())

# Store data in binary form (serialization) under current working directory 
# using pickle.
df_all.to_pickle('results_pickle')

# **b.** Repeat part a for the oral health and dentition data (OHXDEN_*.XPT) 
# retaining the following variables: SEQN, OHDDESTS, tooth counts (OHXxxTC), 
# and coronal cavities (OHXxxCTC).

df_o1 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT')
df_o2 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT')
df_o3 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT')
df_o4 = pd.read_sas('https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT')

# Select needed colunms and add an additional columns for identifying cohorts.
dic_oh = {'2011-2012': df_o1, '2013-2014': df_o2, '2015-2016': df_o3, 
          '2017-2018': df_o4}
df_oh_all = pd.DataFrame()

for k1 in dic_oh.keys():
    # Use regular expression method to find columns with similar names.
    OHXxxTC = re.findall(r'OHX\d+TC', str(list(dic_oh[k1].columns)))
    OHXxxCTC = re.findall(r'OHX\d+CTC', str(list(dic_oh[k1].columns)))
    
    x1 = dic_oh[k1][['SEQN', 'OHDDESTS'] + OHXxxTC + OHXxxCTC].copy()
    x1.loc[:, 'year'] = k1
    
    df_oh_all = pd.concat([df_oh_all, x1], axis=0, ignore_index=True).copy()

# Convert columns to appropriate types.
OHXxxTC_dict = {
    1:'Primary tooth (deciduous) present',
    2:'Permanent tooth present',
    3:'Dental implant',
    4:'Tooth not present',
    5:'Permanent dental root fragment present',
    9:'Could not assess'
    }
OHXxxCTC_dict = {
b'A':'Primary tooth with a restored surface condition',
b'D':'Sound primary tooth',
b'E':'Missing due to dental disease',
b'F':'Permanent tooth with a restored surface condition',
b'J':'Permanent root tip is present but no restorative replacement is present',
b'K':'Primary tooth with a dental carious surface condition',
b'M':'Missing due to other causes',
b'P':'Missing due to dental disease but replaced by a removable restoration',
b'Q':'Missing due to other causes but replaced by a removable restoration',
b'R':'Missing due to dental disease but replaced by a fixed restoration',
b'S':'Sound permanent tooth',
b'T':'Permanent root tip is present but a restorative replacement is present',
b'U':'Unerupted',
b'X':'Missing due to other causes but replaced by a fixed restoration',
b'Y':'Tooth present, condition cannot be assessed',
b'Z':'Permanent tooth with a dental carious surface condition',
b'':'Missing'
    }
OHDDESTS_dict = {
1:'Complete',
2:'Partial',
3:'Not Done'
    }

for c1 in OHXxxTC:
    df_oh_all[c1] = pd.Categorical(df_oh_all[c1].replace(OHXxxTC_dict))
for c2 in OHXxxCTC:
    df_oh_all[c2] = pd.Categorical(df_oh_all[c2].replace(OHXxxCTC_dict))
df_oh_all['OHDDESTS'] = pd.Categorical(df_oh_all['OHDDESTS'].
                                       replace(OHDDESTS_dict))
df_oh_all['SEQN'] = df_oh_all[['SEQN']].astype('int')

# Rename columns.
tooth_cnts = ['Tooth Count: #' + str(i) for i in range(1,33)]
cor_cavities = ['Coronal Caries: Tooth Count #' + str(i) 
                    for i in (list(range(2, 16)) + list(range(18, 32)))]
col_names = ['unique id', 'Dentition Status Code'] + tooth_cnts + cor_cavities
col_names.append('year')
df_oh_all.columns = [n.lower() for n in col_names]

print(df_oh_all.head())

# Store data in binary form (serialization) under current working directory 
# using pickle.
df_oh_all.to_pickle('oh_results_pickle')

# **c.** Report the number of cases there are in the two datasets above.

case1 = len(df_all)
case2 = len(df_oh_all)
print("There are %d cases in the dataset from part a." % case1)
print("There are %d cases in the dataset from part b." % case2)


