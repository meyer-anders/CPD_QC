#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 17:27:42 2017

@author: Anders
"""

import os
import pandas as pd
from ggplot import ggplot, aes, geom_boxplot

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')

df = pd.read_csv('Heme_v3.0_stats.csv')

p = ggplot(df, aes(x='vtype', y = 'faf_cv')) + geom_boxplot()

print(p)