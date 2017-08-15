#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 15:23:32 2017

@author: Anders
"""
import pandas as pd
import os
from functions import compare

print('summarizing variants in each panel')



comparisons = [('Solid_v1.0', 'Solid_v2.0'),
               ('Solid_v1.0', 'PPP_v1.0'),
               ('Solid_v2.0', 'PPP_v1.0'),
               ('Heme_v1.0', 'Heme_v2.0'),
               ('Heme_v1.0', 'Heme_v3.0'),
               ('Heme_v2.0', 'Heme_v3.0')]

panel_summary = compare(comparisons)


os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Summary_stats')
panel_summary.to_csv('panel_overlap.csv', index = False)