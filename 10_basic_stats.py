#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 22:00:47 2017

@author: Anders
"""

import pandas as pd
import os
print('doing stats')
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads8.csv')
panels = pd.read_csv('panels.csv')
variants = pd.read_csv('variants.csv')

reads['faf'] = reads.fad / reads.fdp
stats = reads[['panel_id', 'var_id', 'sample', 'faf', 'fdp', 'seq']]

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')

panel_summary = pd.DataFrame(columns = ['panel', 'num_var', 'num_samples'])

for i, p in panels.iterrows():
    filename = '{}_v{}_stats.csv'.format(p.panel_name, p.panel_version)
    df = stats[stats.panel_id == i]
    df2 = df.groupby(['var_id', 'sample']).agg({'faf': ['count', 'mean', 'std', max, min],
                                       'fdp': ['mean', 'std', max, min]})
    df2.columns = ["_".join(x) for x in df2.columns.ravel()]
    df2['faf_cv'] = df2['faf_std']/df2['faf_mean']
    df2['panel_name'] = p.panel_name
    df2['panel_version'] = p.panel_version
    df2.reset_index(inplace=True)
    
    df2 = df2.merge(variants, how = 'left', on = 'var_id')
    df2.to_csv(filename, index = False)
    panel_summary.loc[i, 'panel'] = '{}_{}'.format(p.panel_name, p.panel_version)
    panel_summary.loc[i, 'num_var'] = len(df['var_id'].copy().drop_duplicates())
    panel_summary.loc[i, 'num_samples'] = len(df['sample'].copy().drop_duplicates())
    

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Summary_stats')
panel_summary.to_csv('var_in_panels.csv', index = False)