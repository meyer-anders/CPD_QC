#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 21:10:41 2017

@author: Anders
"""

import pandas as pd
import os
from functions import parse_sample_name

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/files/Data_exports')
print('parsing sample names')
reads = pd.read_csv('reads2.csv')
reads = parse_sample_name(reads)
reads.to_csv('reads3.csv', index = False)