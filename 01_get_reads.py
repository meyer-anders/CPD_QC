#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 20:30:28 2017

@author: Anders
"""



import pandas as pd
import os
from functions import concat_data


print ('importing data')

directory = '/Users/Anders/Dropbox/Projects/CPD_QC/files/Data_imports/seq_data'

fields = {'Pos': float, 'Alt': str, 'Gene_name': str, 'Chrom_without_chr': str,
          'Effect': str, 'VariantType': str, 'FDP': float, 'FRD': float, 
          'FAD': float,'Sample Sequencing Name': str}

rename = {'Pos' : 'pos', 'Alt' :'alt', 'Gene_name' : 'gene', 
          'Chrom_without_chr' : 'chr', 'Effect' : 'effect',
          'VariantType' : 'vtype', 'FDP' : 'fdp', 'FRD' : 'frd', 'FAD' : 'fad',
          'Sample Sequencing Name' : 'seq_name'}

reads = concat_data(directory, fields)

reads.rename(columns=rename, inplace = True)

reads = reads.dropna(subset = ['pos', 'chr', 'fdp', 'fad', 'frd'])

reads = reads.drop_duplicates(subset = ['pos', 'alt', 'chr', 'seq_name'])

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/files/Data_exports/reads')

reads.to_csv('reads1.csv', index = False)
