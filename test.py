#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:47:02 2017

@author: Anders
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
#from cpd_db_setup2 import SNP, Read, Stats


# SQL setup
engine = create_engine('sqlite:///cpd2.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Data import
original_data = pd.read_excel("validation_full.xlsx")
ash_data = pd.read_csv("fm.sv2_tsca.clincal_only.multirun.csv")
robyn_data1 = pd.read_table("CPDV000386.tab")
robyn_data2 = pd.read_table("CPDV141537.tab")
robyn_data3 = pd.read_table("CPDV151487.tab")
robyn_data4 = pd.read_table("CPDV160726.tab")