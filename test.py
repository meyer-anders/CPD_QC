#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 14:38:15 2017

@author: Anders
"""
import os
import pandas as pd
from pandas.tools.plotting import boxplot_frame_groupby

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
DF = pd.DataFrame()
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        DF = DF.append(df, ignore_index = True)

DF.boxplot('faf_cv', by =['panel_name', 'vtype'])
        