#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 22:47:24 2017

@author: Anders
"""

import pandas as pd
import os
print('setting keys')
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads7.csv')

variants = reads[['chr', 'pos', 'alt']].drop_duplicates().reset_index(drop = True)
variants2 = reads[['chr', 'pos', 'alt', 'gene', 'effect', 'vtype', 'categorization']].\
            drop_duplicates(subset = ['chr', 'pos', 'alt']).reset_index(drop = True)
q = variants.drop_duplicates(subset = ['chr', 'pos'])
merged = variants.merge(q, indicator=True, how='outer')
diff = merged[merged['_merge'] == 'left_only']

variants['var_id'] = variants.index
reads = reads.merge(variants, how = 'left', on = ['chr', 'pos', 'alt'])

panels = reads[['panel_name', 'panel_version']].drop_duplicates().reset_index(drop = True)
panels['panel_id'] = panels.index
reads = reads.merge(panels, how = 'left', on = ['panel_name', 'panel_version'])

variants2 = variants.merge(variants2, how = 'left', on = ['chr', 'pos', 'alt'])
diff.to_csv('mult_alt.csv', index = False)
variants2.to_csv('variants.csv', index = False)
panels.to_csv('panels.csv', index = False)
reads.to_csv('reads8.csv', index = False)

