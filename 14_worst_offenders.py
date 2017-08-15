#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:18:43 2017

@author: Anders
"""

import pandas as pd
import os


print('making panel comparisons')


os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file, usecols = ['var_id','faf_cv','faf_mean','sample', 
                        'fdp_mean','fdp_std', 'gene', 'pos', 'alt', 'faf_count',
                        'categorization'])

        variants_cv = df.groupby('var_id', as_index = False).\
                agg({'faf_cv': 'mean'}).rename(columns = {'faf_cv':'mean_faf_cv'})
        variants_fdp_mean = df.groupby('var_id', as_index = False).\
                agg({'fdp_mean': 'mean'}).rename(columns = {'fdp_mean':'mean_fdp_mean'})
        variants_fdp_std = df.groupby('var_id', as_index = False).\
                agg({'fdp_mean': 'std'}).rename(columns = {'fdp_mean': 'fdp_mean_std'})
        variants_n = df.groupby('var_id', as_index = False).\
                agg({'sample': 'count'}).rename(columns = {'sample':'num_samples'})
        variants_runs = df.groupby('var_id', as_index = False).\
                agg({'faf_count': sum}).rename(columns = {'faf_count':'total_runs'})
        
        variant_info = df[['var_id','gene', 'pos', 'alt', 'categorization']].\
                    copy().drop_duplicates()
        
        variant_summary = variants_cv.merge(variants_fdp_mean, on = 'var_id').\
                                merge(variants_fdp_std, on = 'var_id').\
                                merge(variants_n, on = 'var_id').\
                                merge(variants_runs, on = 'var_id').\
                                merge(variant_info, on = 'var_id')
        
        worst = variant_summary.nlargest(10, 'mean_faf_cv')
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Summary_stats')
        variant_summary.to_csv('summary_{}'.format(file), index = False)
        worst.to_csv('worst_{}'.format(file), index = False)
    
