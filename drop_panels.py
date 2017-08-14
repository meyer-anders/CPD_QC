#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 12:29:21 2017

@author: Anders
"""

import pandas as pd
import os

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')

reads = pd.read_csv('reads4.csv')
panels = reads[['chemistry', 'chem_number', 'panel_name']].drop_duplicates()


panels_to_keep = ['FFPE_V1.1', 'HEME_V1.2', 'HEMEao_V1.3', 'PPP', 'Solid', 'bPPP']
reads = reads.loc[(reads.panel_name.isin(panels_to_keep)) | 
        (reads.chemistry.isin(panels_to_keep)), :]


reads.to_csv('reads5.csv', index = False)

