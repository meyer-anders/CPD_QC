#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 09:30:08 2017

@author: Anders

to do:
    fix sample, seq barcoding
    add filters
    
"""
import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import SNP, Read


Base = declarative_base()
engine = create_engine('sqlite:///cpd2.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

data = pd.read_excel("validation_full.xlsx")
data.dropna(subset = ['dbsnp', 'FDP', 'FRD', 'FAD'], inplace = True)
data_rows = len(data)

#==============================================================================
# Loads reads
#==============================================================================

for r in range(data_rows):
    sample = data["sample name"].iloc[r]
    split = sample.split("-")
    run_barcode = int(split[-1] + split[-3] + split[-7])
    snp = session.query(SNP).filter_by(dbsnp = data.dbsnp.iloc[r]).first()
    new_read = Read(fdp = int(data.FDP.iloc[r]),
                    frd = int(data.FRD.iloc[r]),
                    fad = int(data.FAD.iloc[r]),
                    snp = snp,
                    run = run_barcode,
                    panel = split[-8],
                    sample = split[0])
    new_read.faf = new_read.fad / new_read.fdp 
    session.add(new_read)
    session.commit()
    
session.close()