#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 23:11:44 2017

@author: Anders
"""
import numpy as np
import pandas as pd

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
df = pd.read_csv('Heme_v1.0_stats.csv').dropna(subset = ['faf_mean', 'faf_std', 
                'faf_count'])
df = df.loc[df.faf_std>0, :].reset_index(drop=True)
nsamples = 0
nrows = len(df)
samples = pd.Series()
while nsamples < 10000:
    r = np.random.randint(0, nrows)
    mean = df.loc[r, 'faf_mean']
    s = pd.Series(np.random.normal(mean, df.loc[r, 'faf_std'], 
                                   df.loc[r, 'faf_count']))
    
    samples = samples.append((s>1.5*mean) | (s<mean/1.5) )
    nsamples += len(s)
    
