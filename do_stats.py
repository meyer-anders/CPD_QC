#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 22:00:47 2017

@author: Anders
"""

import pandas as pd
import os

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads8.csv')
panels = pd.read_csv('panels.csv')
variants = pd.read_csv('variants.csv')

reads['faf'] = reads.fad / reads.fdp
stats = reads[['panel_id', 'var_id', 'faf', 'fdp', 'seq']]

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
for i, p in panels.iterrows():
    filename = '{}_v{}_stats.csv'.format(p.panel_name, p.panel_version)
    df = stats[stats.panel_id == 1]
    df2 = df.groupby('var_id').agg({'faf': ['count', 'mean', 'std', max, min],
                                       'fdp': ['mean', 'std', max, min]})
    df2[('faf','cv')] = df2[('faf', 'std')]/df2[('faf', 'mean')]
    df2 = df2.merge(variants, how = 'left', left_index = True, right_index = True)
    df2.to_csv(filename, index = False)



#panel_stats = reads.groupby(['chr', 'pos', 'alt']).agg(lambda x: set(x.values))


