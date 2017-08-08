#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 21:14:04 2017

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
Base = declarative_base()
#engine = create_engine('mysql+pymysql://root@localhost:3306/cpd', echo=False)
engine = create_engine('sqlite:///CPD.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def make_plot(x, df, cutoffs):
    bins = pd.DataFrame(columns = ['lower', 'upper', 'y'])
    for i in range(len(cutoffs)-1):
        upper = cutoffs[i+1]
        lower = cutoffs[i]
        bins.set_value(i, 'upper', str(int(upper*100)))
        bins.set_value(i, 'lower', str(int(lower*100)))
        subset = df[df[x]< upper ]
        subset = subset[subset[x]> lower]
        y = subset['faf_cv']
        bins.set_value(i, 'y', y)
    return bins

q = session.query(Stats).filter_by(panel = 'bPPP')
df = pd.read_sql_query(q.statement, engine)
bins = make_plot('faf_mean', df, faf_cutoffs)