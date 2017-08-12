#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:46:36 2017

@author: Anders
"""
import pandas as pd
import numpy as np
import os
from functions import parse_sample_name

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads.csv')

'''
CLEAR OUT FAILED RUNS, FLAG OTHER POTENTIAL FAILED RUNS
'''
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')
c = {'Sample Sequencing Name': str, 'Panel_name': str }
failed_runs = pd.read_table("failed seq QC data.tab", dtype = c,
                            usecols = c.keys())
failed_runs = failed_runs.dropna(subset = ['Sample Sequencing Name'])
print('data loaded')

runs_to_drop = set(failed_runs['Sample Sequencing Name'].drop_duplicates())
runs = set(reads['Sample Sequencing Name'].drop_duplicates())
runs_to_drop = list(runs_to_drop & runs)
n = 0
for r in runs_to_drop:
    reads = reads[reads['Sample Sequencing Name'] != r]
    n +=1
    print('{} of {} rows deleted'.format(n, len(runs_to_drop)))

# flag other potential failed runs
reads.flagged = False
repeat_runs = reads[reads.repeat == True].\
    drop_duplicates(subset = ['Sample Sequencing Name'])

n = 0
for i, r in repeat_runs.iterrows():
    reads.loc[(reads.chemistry == r.chemistry) &
            (reads.chem_number == r.chem_number) &
            (reads.repeat == False), 'flagged'] = True
    n +=1
    print('{} of {} rows flagged'.format(n, len(repeat_runs)))

'''
GET PANEL NAMES
'''

failed_runs = parse_sample_name(failed_runs)
failed_runs = failed_runs.loc[:,['chemistry', 'chem_number', 'Panel_name']].drop_duplicates()

reads.Panel_name = np.nan
n = 0
for i, r in failed_runs.iterrows():
    reads.loc[(reads.chemistry == r.chemistry) &
              (reads.chem_number == r.chem_number), 'Panel_name'] = r.Panel_name
    n +=1
    print('{} of {} rows named'.format(n, len(failed_runs)))

panels_w_samples = reads.loc[:,['sample', 'chemistry', 'chem_number', 'Panel_name']].\
                drop_duplicates()

panels = panels_w_samples.loc[:,['chemistry', 'chem_number', 'Panel_name']].\
                drop_duplicates()

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads.to_csv('reads.csv', index = False)
panels_w_samples.to_csv('panels_w_samples.csv', index = False)
panels.to_csv('panels.csv', index = False)