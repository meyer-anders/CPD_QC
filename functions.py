#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:38:45 2017

@author: Anders
"""
import numpy as np
import pandas as pd

def parse_sample_name(df):
    df.sample = np.nan
    df.chemistry = np.nan
    df.chem_number = np.nan
    df.pal = np.nan
    df.seq = np.nan
    df.repeat = np.nan
    names = df.drop_duplicates(subset = ['Sample Sequencing Name'])
    n = 0
    for i, r in names.iterrows():
        sample_name = r["Sample Sequencing Name"]
        split = sample_name.split("-")
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'sample'] = split[0]
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'chemistry'] = split[-8]
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'chem_number'] = split[-7]
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'pal'] = split[-3]
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'seq'] = split[-1]
        df.loc[df['Sample Sequencing Name'] == sample_name, \
            'repeat'] = (split[1] == 'A')
        n += 1
        print('{} of {} rows parsed'.format(n, len(names)))
    
    
    #drop inapprpriate non-numeric entries
    df['chem_number'] = pd.to_numeric(df['chem_number'], errors = 'coerce').\
                        fillna(0).astype(int)
    return df