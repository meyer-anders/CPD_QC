#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 10:43:29 2017

@author: Anders
"""

import pandas as pd
import numpy as np
import os

print('revising panel versions')
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')

reads = pd.read_csv('reads5.csv')

reads.panel_version = np.nan

reads.loc[(reads.chemistry == 'Solid'), 'panel_name2'] = 'Solid'
reads.loc[(reads.chemistry == 'Solid'), 'panel_version'] = 2
reads.loc[(reads.chemistry == 'bPPP'), 'panel_name2'] = 'PPP'
reads.loc[(reads.panel_name2 == 'PPP'), 'panel_version'] = 1

runs = reads[['seq_name','panel_name', 'panel_version']].drop_duplicates()
                     
panel_summary = pd.pivot_table(runs, values = 'seq_name', columns='panel_name', 
                               aggfunc=len, fill_value = 0)

panel_summary.rename('num_runs', inplace = True)

panel_summary.to_csv('panel_summary.csv', header = True)

panels_to_keep = ['FFPE_V1.1', 'HEME_V1.2', 'HEMEao_V1.3', 'PPP', 'Solid', 'bPPP']

panel_rename_dict = {'FFPE_V1.1' : ('Solid',1),
                     'HEME_V1.1' : ('Heme', 1),
                     'HEME_V1.2' : ('Heme', 0),
                     'HEME_V2.0' : ('Heme', 0),
                     'HEMEao_V1.3' : ('Heme', 3)}

for k, v in panel_rename_dict.items():
    reads.loc[(reads.panel_name == k), 'panel_name2'] = v[0]
    reads.loc[(reads.panel_name == k), 'panel_version'] = v[1]

reads.loc[(reads.panel_version == 0) &
          (reads.year >= 15) &
          (reads.acc_num >841), 'panel_version'] = 3

reads.loc[reads['panel_version'] == 0, 'panel_version'] = 2

reads.drop('panel_name', axis = 1, inplace = True)
reads.rename(columns = {'panel_name2': 'panel_name'}, inplace = True)

panels = reads[['panel_name', 'panel_version']].drop_duplicates()

reads.to_csv('reads6.csv', index = False)


