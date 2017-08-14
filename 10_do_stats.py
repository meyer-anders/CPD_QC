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
stats = reads[['panel_id', 'var_id', 'faf', 'fdp', 'seq']]

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
panel_summary = pd.DataFrame(columns = ['panel', 'overlap', 'num_var'])

for i, p in panels.iterrows():
    filename = '{}_v{}_stats.csv'.format(p.panel_name, p.panel_version)
    df = stats[stats.panel_id == i]
    df2 = df.groupby('var_id').agg({'faf': ['count', 'mean', 'std', max, min],
                                       'fdp': ['mean', 'std', max, min]})
    df2.columns = ["_".join(x) for x in df2.columns.ravel()]
    df2['faf_cv'] = df2['faf_std']/df2['faf_mean']
    df2['panel_name'] = p.panel_name
    df2['panel_version'] = p.panel_version
    df2 = df2.merge(variants, how = 'left', left_index = True, right_index = True)
    panel_summary.loc[i, 'panel'] = '{}_{}'.format(p.panel_name, p.panel_version)
    panel_summary.loc[i, 'num_var'] = len(df2)
    df2.to_csv(filename, index = False)

solid1 = pd.read_csv('Solid_v1.0_stats.csv')
solid2 = pd.read_csv('Solid_v2.0_stats.csv')
ppp = pd.read_csv('PPP_v1.0_stats.csv')

joined = solid1.merge(solid2, how ='inner', on = 'var_id')
panel_line = pd.Series({'panel':'Solid_v1.0', 'overlap' : 'Solid_v2.0', 
                        'num_var': len(joined)})
panel_summary = panel_summary.append(panel_line, ignore_index = True)

joined = solid1.merge(ppp, how ='inner', on = 'var_id')
panel_line = pd.Series({'panel':'Solid_v1.0', 'overlap' : 'PPP_v1.0', 
                        'num_var': len(joined)})
panel_summary = panel_summary.append(panel_line, ignore_index = True)

joined = solid2.merge(ppp, how ='inner', on = 'var_id')
panel_line = pd.Series({'panel':'Solid_v2.0', 'overlap' : 'PPP_v1.0', 
                        'num_var': len(joined)})
panel_summary = panel_summary.append(panel_line, ignore_index = True)

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
panel_summary.to_csv('var_in_panels.csv', index = False)
