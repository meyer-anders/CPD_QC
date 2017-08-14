#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 22:47:24 2017

@author: Anders
"""

import pandas as pd
import os

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads7.csv')

variants = reads[['chr', 'pos', 'alt']].drop_duplicates()
q = variants.drop_duplicates(subset = ['chr', 'pos'])
merged = variants.merge(q, indicator=True, how='outer')
diff = merged[merged['_merge'] == 'left_only']

variants['var_id'] = variants.index
joined = reads.merge(variants, how = 'left', on = ['chr', 'pos', 'alt'])


diff.to_csv('mult_alt.csv', index = False)
variants.to_csv('variants.csv', index = False)
joined.to_csv('reads8.csv', index = False)

