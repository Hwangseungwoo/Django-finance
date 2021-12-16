#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np  
import json
import codecs
import csv
from pandas import json_normalize
from math import log
import re
import os
from konlpy.tag import Okt
from collections import Counter
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import warnings
warnings.filterwarnings(action='ignore')

cwd = os.getcwd()  # Get the current working directory (cwd)

path = './pybo/base/수시입출금_가중치완료_데모변수_추출완료.csv'



def recommend_product(age, gender):
    df = pd.read_csv(path, encoding='utf-8') 
    age = int(age)
    gender = int(gender)
    
    if age < 20 : 
        df1 = df[(df['나이2'] == '') | (df['10대'] == 1)]
    elif age < 30 :
        df1 = df[(df['나이2'] == '') | (df['20대'] == 1)]
    elif age < 40 :
        df1 = df[(df['나이2'] == '') | (df['30대'] == 1)]
    elif age < 50 : 
        df1 = df[(df['나이2'] == '') | (df['40대'] == 1)]
    elif age < 60 :
        df1 = df[(df['나이2'] == '') | (df['50대'] == 1)]
    elif age < 70 :
        df1 = df[(df['나이2'] == '') | (df['60대'] == 1)]
    else: 
        df1 = df[(df['나이2'] == '') | (df['70대'] == 1)]
        
    if gender == 1:
        df2 = df1[df1['성별'] != 'W']
    else:
        df2 = df1[df1['성별'] != 'M']

    df_final = df2.sort_values(by='기본금리', ascending=False).head(3)
    lst = []
    a = df_final.to_dict('records')
    lst.append(a)
    return lst

