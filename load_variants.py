#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 08:34:21 2017

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



# Data import
fields = {'Pos': int, 'Alt': str, 'Gene_name': str, 'Chrom_without_chr': str,
          'Effect': str, 'VariantType': str}
variants = pd.read_csv('variants.csv', dtype = fields)

# load variants, no duplicates left in data
nvars = len(variants)
for r in range(nvars):
    new_var = Variant(position = int(variants.Pos.iloc[r]),
                      nucleotide = variants.Alt.iloc[r],
                      gene = variants.Gene_name.iloc[r],
                      chromosome = variants.Chrom_without_chr.iloc[r],
                      effect = variants.Effect.iloc[r],
                      var_type = variants.VariantType.iloc[r])
    session.add(new_var)
    
session.commit()  

session.close()
