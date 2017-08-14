#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 20:36:30 2017

@author: Anders
"""

import pandas as pd
import os

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads6.csv')
categories = pd.read_csv('categories.csv')

joined = reads.merge(categories, how = 'left',
                        on = ['chr', 'pos', 'alt'])
joined = joined.drop_duplicates(subset = ['chr', 'pos', 'alt', 'seq_name'])

joined.to_csv('reads7.csv', index = False)