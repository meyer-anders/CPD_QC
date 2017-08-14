#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:18:43 2017

@author: Anders
"""

import pandas as pd
import numpy as np
import os


print('making panel comparisons')


os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file, usecols = ['faf_cv', 'faf_mean', 'fdp_mean',
                         'gene', 'pos']).nlargest(10, columns = 'faf_cv')
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
        df.to_csv('worst_{}'.format(file))
    
