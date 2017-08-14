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
    df.year = np.nan
    df.acc_num = np.nan
    names = df.seq_name.drop_duplicates()
    n = 0
    t = len(names)
    for r in names:
        sample_name = r
        split = sample_name.split("-")
        mask = df.seq_name == sample_name
        d = {'sample': str(split[0]),
             'chemistry' : str(split[-8]),
             'chem_number' : int(str(split[-7])),
             'pal' : int(str(split[-3])),
             'seq' : int(str(split[-1])),
             'repeat' : (str(split[1]) == 'A'),
             'year' : int(split[0][4:6]),
             'acc_num' : int(split[0][6:])}
        for k, v in d.items():
            df.loc[mask, k] = v
        
        n += 1
        if n%100 ==0:print('{} of {} rows parsed'.format(n, t))
    
    
    #drop inapprpriate non-numeric entries
    df['chem_number'] = pd.to_numeric(df['chem_number'], errors = 'coerce').\
                        fillna(0).astype(int)
    return df