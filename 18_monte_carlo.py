#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 23:11:44 2017

@author: Anders
"""
import pandas as pd
import os
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')

total = 100000
clin_change = 0.3
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        panel_name = df.panel_name[0]
        panel_version = df.panel_version[0]
        df = df.dropna(subset = ['faf_mean', 'faf_std', 'faf_count'])
        df = df.loc[df.faf_std>0, :].reset_index(drop=True)
        
        nsamples = 0
        nrows = len(df)
        samples = pd.Series()
        while nsamples < total:
            r = np.random.randint(0, nrows)
            mean = df.loc[r, 'faf_mean']
            s = pd.Series(np.random.normal(mean, df.loc[r, 'faf_std'], 
                                           df.loc[r, 'faf_count']))
            samples = samples.append((s>(1+clin_change)*mean) | 
                                    (s<mean*(1-clin_change)) )
            nsamples += len(s)
        
        samples = samples[:total] 
        sim = pd.DataFrame(columns=['s', 'surviving'])
        sim['s'] = samples
        sim = sim.reset_index(drop = True)

        for i in range(total): 
            sim.loc[i, 'surviving'] = (nrows - sum(sim.s[:i]))/nrows
        
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Simulations')
        sim.to_csv('{}_{}_{}_simulation.csv'.format(panel_name, panel_version, 
                   total), index = False)



