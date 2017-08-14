#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
Created on Fri Aug  4 15:01:19 2017

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


fields = {'Pos': int, 'Alt': str, 'Chrom_without_chr': str,
          'Categorization': str}
categ = pd.read_csv('categ.csv', dtype = fields)

nrows = len(categ)
for r in range(nrows):
    q = session.query(Variant).filter(
            Variant.chromosome == categ.Chrom_without_chr.iloc[r],
            Variant.position == int(categ.Pos.iloc[r]),
            Variant.nucleotide == categ.Alt.iloc[r])
    if session.query(q.exists()).scalar():
        v = q.first()
        v.categ = categ.Categorization.iloc[r]
session.commit()

session.close()
