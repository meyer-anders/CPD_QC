#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:52:37 2017

@author: Anders
"""

import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import SNP, Read, Stats

# SQL setup
Base = declarative_base()
engine = create_engine('sqlite:///cpd2.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


panels = []
for i in session.query(Read.panel).distinct():
    panels.append(i.panel)
    

snps = session.query(SNP).all()


for p in panels:
    for snp in snps:
        reads = session.query(Read).filter_by(snp_id=snp.id)
        df = pd.read_sql_query(reads.statement, engine)
        df = df[df['panel']==p]
        if len(df) > 0:
            new_stat = Stats(snp = snp,
                            panel = p,
                            depth_mean = df.fdp.mean(),
                            faf_mean = df.faf.mean(),
                            faf_sd = df.faf.std(),
                            faf_cv = df.faf.std()/df.faf.mean(),
                            num_runs = len(df))
            session.add(new_stat)
            session.commit()
session.close()

