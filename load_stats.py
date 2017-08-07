#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:52:37 2017

@author: Anders

CAUTION: This must start with a blank table! 
        There is no protection against duplicates!
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


panels = []
for i in session.query(Read.panel).distinct():
    panels.append(i.panel)

samples = []
for i in session.query(Read.sample).distinct():
    samples.append(i.sample)

stats = []

for s in samples:
    variants = session.query(Read.var_id).filter_by(sample = s).distinct().all()
    reads = session.query(Read).filter(Read.sample==s)
    df2 = pd.read_sql_query(reads.statement, engine)
    for v in variants:
        df = df2.loc[df2.var_id == v, :]
        mean = df.faf.mean()
        std = df.faf.std()
        if len(df) > 1 and mean >0: # summary stats across panels
            new_stat = {'var_id' : v.var_id,
                        'panel' : 'all',
                        'sample' : s,
                        'fdp_mean' : df.fdp.mean(),
                        'faf_mean' : mean,
                        'faf_sd' : std,
                        'faf_cv' : std/mean,
                        'num_runs' : len(df)}
            stats.append(new_stat)

        for p in panels: # for each panel
            df = df.loc[df.panel == p, :]
            mean = df.faf.mean()
            std = df.faf.std()
            if len(df) > 1 and mean >0:
                new_stat = {'var_id' : v.var_id,
                            'panel' : p,
                            'sample' : s,
                            'fdp_mean' : df.fdp.mean(),
                            'faf_mean' : mean,
                            'faf_sd' : std,
                            'faf_cv' : std/mean,
                            'num_runs' : len(df)}
                stats.append(new_stat)
    for s in stats: session.add(Stats(**s))
    session.commit()
    stats = []

            
session.close()

