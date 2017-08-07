#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 12:34:35 2017

@author: Anders
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import Variant, Read, Stats


# SQL setup
#engine = create_engine('mysql+pymysql://root@localhost:3306/cpd', echo=False)
engine = create_engine('sqlite:///CPD.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

fields = {'Pos': int, 'Alt': str, 'Chrom_without_chr': str, 'FDP': int, 
          'FRD': int, 'FAD': int,'Sample Sequencing Name': str}

reads = pd.read_csv('reads.csv')
reads = reads.astype(dtype=fields)
nrows = len(reads)

reads_list = []
for r in range(nrows):
    var = session.query(Variant.id).filter(
            Variant.position == int(reads.Pos.iloc[r]),
            Variant.nucleotide == reads.Alt.iloc[r],
            Variant.chromosome == reads.Chrom_without_chr.iloc[r]).first()
    sample = reads["Sample Sequencing Name"].iloc[r]
    split = sample.split("-")
    run_barcode = int(split[-1] + split[-3] + split[-7])
    new_read = {
            'fdp' : int(reads.FDP.iloc[r]),
            'frd' : int(reads.FRD.iloc[r]),
            'fad' : int(reads.FAD.iloc[r]),
            'var_id' : var.id,
            'run' : int(run_barcode),
            'panel' : split[-8],
            'sample' : split[0],
            'faf' : reads.FAD.iloc[r]/reads.FDP.iloc[r]
            }
    reads_list.append(new_read)

for r in reads_list: session.add(Read(**r))
session.commit()

session.close()