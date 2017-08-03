#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 08:34:21 2017

@author: Anders

To do:
    correct dbsnp
    put into functions
    run functions for each data set
    protect against duplicates

this version will ignore categorization
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import Variant, Read, Stats


# SQL setup
engine = create_engine('sqlite:///cpd2.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_new_var(data, r):
    new_var = Variant(position = int(data.Pos.iloc[r]),
                          nucleotide = data.Alt.iloc[r],
                          gene = data.Gene_name.iloc[r],
                          chromosome = data.Chrom_without_chr.iloc[r],
                          effect = data.Effect.iloc[r],
                          var_type = data.VariantType.iloc[r])
    q = session.query(Variant).filter(Variant.position == new_var.position,
                                         Variant.nucleotide == new_var.nucleotide,
                                         Variant.chromosome == new_var.chromosome)
    if not session.query(q.exists()).scalar():
        session.add(new_var)
        session.commit()  
    return

def add_new_read(data,r):
    sample = data["Sample Sequencing Name"].iloc[r]
    split = sample.split("-")
    run_barcode = int(split[-1] + split[-3] + split[-7])
    q = session.query(Variant).filter(Variant.position == int(data.Pos.iloc[r]),
                                         Variant.nucleotide == data.Alt.iloc[r],
                                         Variant.chromosome == data.Chrom_without_chr.iloc[r])
    var = q.first()
    new_read = Read(fdp = int(data.FDP.iloc[r]),
                    fad = int(data.FAD.iloc[r]),
                    var = var,
                    run = run_barcode,
                    panel = split[-8],
                    sample = split[0])
    new_read.faf = new_read.fad / new_read.fdp 
    q2 = session.query(Read).filter(Read.var == new_read.var,
                                    Read.run == new_read.run,
                                    Read.panel == new_read.panel,
                                    Read.sample == new_read.sample,
                                    Read.fdp == new_read.fdp)
    if not session.query(q2.exists()).scalar():
        session.add(new_read)
        session.commit()
    return



def load_data(data):
    data.dropna(subset = ['Pos', 'FDP', 'FAD'], inplace = True)
    data_rows = len(data)
    for r in range(data_rows):
        add_new_var(data, r)
        add_new_read(data, r)
    return


# Data import

original_data = pd.read_excel("validation_full.xlsx")
ash_data = pd.read_csv("fm.sv2_tsca.clincal_only.multirun.csv")
CPDV000386 = pd.read_table("CPDV000386.tab")
CPDV141537 = pd.read_table("CPDV141537.tab")
CPDV151487 = pd.read_table("CPDV151487.tab")
CPDV160726 = pd.read_table("CPDV160726.tab")
heme_data = pd.read_csv("heme pos ctl.csv")


load_data(original_data)
load_data(ash_data)
load_data(CPDV000386)
load_data(CPDV141537)
load_data(CPDV151487)
load_data(CPDV160726)
load_data(heme_data)

session.close()
