#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 12:34:35 2017

@author: Anders
"""

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, aliased
#from sqlalchemy import create_engine, exists, func
#from cpd_db_setup2 import Variant, Read, Stats
#
#
## SQL setup
##engine = create_engine('mysql+pymysql://root@localhost:3306/cpd', echo=False)
#engine = create_engine('sqlite:///CPD.db')
#Base = declarative_base(bind=engine)
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

fields = {'Pos': int, 'Alt': str, 'Chrom_without_chr': str, 'FDP': int, 
          'FRD': int, 'FAD': int,'Sample Sequencing Name': str}

reads = pd.read_csv('reads.csv')
reads = reads.astype(dtype=fields)
reads['run'] = np.nan
reads['panel'] = np.nan
reads['sample'] = np.nan
reads['FAF'] = np.nan
nrows = len(reads)


for r in range(nrows):
    sample = reads["Sample Sequencing Name"].iloc[r]
    split = sample.split("-")
    run_barcode = int(split[-1] + split[-3] + split[-7])
    df.iloc[r, df.columns.get_loc('run')] = int(run_barcode)
    df.iloc[r, df.columns.get_loc('panel')] = split[-8]
    df.iloc[r, df.columns.get_loc('sample')] = split[0]
    df.iloc[r, df.columns.get_loc('FAF')] = reads.FAD.iloc[r] / reads.FDP.iloc[r]
