#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 21:36:19 2017

@author: Anders


Drops and types columns
"""

import pandas as pd
import os
import numpy as np
from functions import parse_sample_name

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')
'''
SEQUENCING DATA
'''
fields = {'Pos': float, 'Alt': str, 'Gene_name': str, 'Chrom_without_chr': str,
          'Effect': str, 'VariantType': str, 'FDP': float, 'FRD': float, 
          'FAD': float,'Sample Sequencing Name': str}


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
print('data loaded')

'''
COMBINE, DROP NA, DROP DUPLICATES, PARSE SAMPLE NAME
'''
final = pd.DataFrame()
for df in dfs:
   final = final.append(df, ignore_index = True)

print('data combined')

final = final.dropna(subset = ['Pos', 'Chrom_without_chr'])

reads = final[['Pos', 'Alt', 'Chrom_without_chr', 'FDP', 'FRD', 'FAD',
               'Sample Sequencing Name']]
reads = reads.drop_duplicates(subset = ['Pos', 'Alt', 'Chrom_without_chr', 
                                        'Sample Sequencing Name'])
variants = final[['Pos', 'Alt', 'Chrom_without_chr', 'Effect', 
                  'VariantType', 'Gene_name']]
variants = variants.drop_duplicates(subset = ['Pos', 'Alt', 'Chrom_without_chr'])
reads = reads.dropna(subset = ['FDP', 'FAD', 'FRD'])
print('duplicates dropped')
reads = parse_sample_name(reads)
print('reads parsed')




'''
CATEGORIZATION DATA
'''
fields = {'Pos': float, 'Alt': str, 'Chrom_without_chr': str,
          'Categorization': str}
categ = pd.read_table('ReportedVariants.tab', dtype = fields, 
                      usecols = fields.keys())
categ = categ.dropna(subset = ['Pos', 'Chrom_without_chr', 'Categorization'])
categ = categ.drop_duplicates(subset = ['Pos', 'Alt', 'Chrom_without_chr'])
print('categorization done')



'''
DATA OUTPUT
'''
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
variants.to_csv('variants.csv', index = False)
reads.to_csv('reads.csv', index = False)
categ.to_csv('categ.csv', index = False)



    
