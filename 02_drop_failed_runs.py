#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:50:29 2017

@author: Anders
"""

import pandas as pd
import os
print('dropping failed runs')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/files/Data_imports/failed_runs')

c = {'Sample Sequencing Name': str, 'Panel_name': str }
failed_runs = pd.read_table("failed seq QC data.tab", dtype = c,
                            usecols = c.keys())
rename = {'Pos' : 'pos', 'Alt' :'alt', 'Gene_name' : 'gene', 
          'Chrom_without_chr' : 'chr', 'Effect' : 'effect',
          'VariantType' : 'vtype', 'FDP' : 'fdp', 'FRD' : 'frd', 'FAD' : 'fad',
          'Sample Sequencing Name' : 'seq_name'}
failed_runs.rename(columns = rename, inplace = True)

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads1.csv')
runs = reads.seq_name.drop_duplicates()

failed_runs = failed_runs.dropna(subset = ['seq_name'])

common = reads.merge(failed_runs,on=['seq_name'])

reads = reads[~reads.seq_name.isin(common.seq_name)]

reads.to_csv('reads2.csv', index = False)
common.to_csv('failed_runs.csv', index = False)