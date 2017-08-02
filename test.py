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


# SQL setup
engine = create_engine('sqlite:///cpd2.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Data import
original_data = pd.read_excel("validation_full.xlsx")
ash_data = pd.read_csv("fm.sv2_tsca.clincal_only.multirun.csv")
CPDV000386 = pd.read_table("CPDV000386.tab")
CPDV141537 = pd.read_table("CPDV141537.tab")
CPDV151487 = pd.read_table("CPDV151487.tab")
CPDV160726 = pd.read_table("CPDV160726.tab")
heme_data = pd.read_csv("heme pos ctl.csv")