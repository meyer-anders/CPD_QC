#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 12:29:21 2017

@author: Anders
"""

import pandas as pd
import os

print('dropping panels')
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')

reads = pd.read_csv('reads4.csv')
panels_before_drop = reads[['chemistry', 'chem_number', 'panel_name']].drop_duplicates()


panels_to_keep = ['FFPE_V1.1', 'HEME_V1.2', 'HEMEao_V1.3', 'HEME_V1.1', 
                  'HEME_V2.0', 'PPP', 'Solid', 'bPPP']
reads = reads.loc[(reads.panel_name.isin(panels_to_keep)) | 
        (reads.chemistry.isin(panels_to_keep)), :]

panels_after_drop = reads[['chemistry', 'chem_number', 'panel_name']].drop_duplicates()

dropped_panels = panels_before_drop[~panels_before_drop.index.\
                                    isin(panels_after_drop.index)].drop_duplicates()
reads.to_csv('reads5.csv', index = False)
dropped_panels.to_csv('dropped_panels.csv', index = False)

