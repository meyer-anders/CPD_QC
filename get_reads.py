#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:30:28 2017

@author: Anders
"""



import pandas as pd
import os


print ('importing data')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')
'''
SEQUENCING DATA
'''
fields = {'Pos': float, 'Alt': str, 'Gene_name': str, 'Chrom_without_chr': str,
          'Effect': str, 'VariantType': str, 'FDP': float, 'FRD': float, 
          'FAD': float,'Sample Sequencing Name': str}

rename = {'Pos' : 'pos', 'Alt' :'alt', 'Gene_name' : 'gene', 
          'Chrom_without_chr' : 'chr', 'Effect' : 'effect',
          'VariantType' : 'vtype', 'FDP' : 'fdp', 'FRD' : 'frd', 'FAD' : 'fad',
          'Sample Sequencing Name' : 'seq_name'}


original_data = pd.read_excel("validation_full.xlsx", converters = fields, usecols = fields.keys())
CPDV000386 = pd.read_table("CPDV000386.tab", dtype = fields, usecols = fields.keys())
CPDV141537 = pd.read_table("CPDV141537.tab", dtype = fields, usecols = fields.keys())
CPDV151487 = pd.read_table("CPDV151487.tab", dtype = fields, usecols = fields.keys())
CPDV160726 = pd.read_table("CPDV160726.tab", dtype = fields, usecols = fields.keys())
heme_data = pd.read_csv("heme pos ctl.csv", dtype = fields, usecols = fields.keys())
ash_data = pd.read_csv("fm.sv2_tsca.clincal_only.multirun.csv", 
                       dtype = fields, usecols = fields.keys())
CPDV170682 = pd.read_table("CPDV170682_HEME_pos_ctl_2.tab", 
                           dtype = fields, usecols = fields.keys())

dfs = [original_data, CPDV000386, CPDV141537, CPDV151487, CPDV160726, 
       heme_data, ash_data, CPDV170682]

reads = pd.DataFrame()
for df in dfs:
   reads = reads.append(df, ignore_index = True)

reads.rename(columns=rename, inplace = True)


reads = reads.dropna(subset = ['pos', 'chr', 'fdp', 'fad', 'frd'])

reads = reads.drop_duplicates(subset = ['pos', 'alt', 'chr', 'seq_name'])

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads.to_csv('reads1.csv', index = False)
