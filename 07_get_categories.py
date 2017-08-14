#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 19:16:38 2017

@author: Anders
"""

import pandas as pd
import os

print('getting categories')
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')

categ = pd.read_table('ReportedVariants.tab', 
                      usecols = ['Chrom_without_chr', 'Pos', 'Alt', 
                        'Categorization']).dropna(subset = ['Categorization']).\
                        drop_duplicates()
rename = {'Pos' : 'pos', 'Alt' :'alt', 'Chrom_without_chr' : 'chr', 
          'Categorization' : 'categorization'}
categ.rename(columns = rename, inplace = True)

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
categ.to_csv('categories.csv', index = False)

