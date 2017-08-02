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





"""
import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import SNP, Read, Stats
from getkey import getkey, keys

# SQL setup
engine = create_engine('sqlite:///cpd2.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Data import
data = pd.read_excel("validation_full.xlsx")
data.dropna(subset = ['dbsnp'], inplace = True)
categorization = pd.read_excel("alt_categorization.xlsx")
data_rows = len(data)
cat_rows = len(categorization)


#==============================================================================
# Load all the snps into the database and prevent duplicate entries
#==============================================================================
cats = []
snps = [] # will need to update this to load from the database to prevent dups
for r in range(data_rows):
    new_snp = int(data.dbsnp.iloc[r])
    if not new_snp in snps:
        snps.append(new_snp) #add dbsnp to list to prevent adding dups
        new_SNP = SNP(dbsnp = new_snp,
                      gene = data.Gene_name.iloc[r],
                      chromosome = data.Chrom_without_chr.iloc[r],
                      effect = data.Effect.iloc[r],
                      var_type = data.VariantType.iloc[r])
        for c in range(cat_rows): #add categorization
            if categorization.cDNA.iloc[c] == data["cDNA change"].iloc[r]:
                new_SNP.categ = categorization.categorization.iloc[c]
                cats.append(new_SNP.dbsnp) # this is just to check that all the cats were added
                break
        session.add(new_SNP)
session.commit()
session.close()
