#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 12 13:19:18 2017

@author: Anders
"""

import pandas as pd
import numpy as np
import os


os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')
panels = pd.read_csv('library preps.csv', header = None, usecols = [23,28],
                     names = ['panel_name', 'panel_id'])
panels = panels.dropna().drop_duplicates()

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads3.csv')
reads.panel_name = np.nan

n = 0
t = len(panels)
for i, r in panels.iterrows():
    sample_name = str(r[1])
    split = sample_name.split("_")
    chemistry = str(split[0])
    chem_number = int(str(split[1])) 
    reads.loc[(reads.chemistry == str(split[0])) &
              (reads.chem_number == int(str(split[1]))), 'panel_name'] \
              = str(r.panel_name)
    n +=1
    if n%100 == 0: print('{} of {} rows named'.format(n, t))

reads.to_csv('reads4.csv', index = False)