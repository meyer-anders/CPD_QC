#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 15:20:33 2017

@author: Anders
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///cpd2.db')
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
 

# change to correct dbsnp nonsense
class SNP(Base):
    __tablename__ = "snp"
    id = Column(Integer, primary_key=True)
    dbsnp = Column(Integer)
    gene = Column(String(250))
    chromosome = Column(String(250))
    effect = Column(String(250))
    var_type = Column(String(250))
    categ = Column(String(250))

# add quality score where available.
class Read(Base):
    __tablename__ = "read"
    id = Column(Integer, primary_key = True)
    fdp = Column(Integer)
    frd = Column(Integer)
    fad = Column(Integer)
    faf = Column(Float)
    panel = Column(String(250))
    sample = Column(String(250))
    run = Column(Integer) # fix to make seq id
    snp_id = Column(Integer, ForeignKey("snp.id"))
    snp = relationship(SNP, backref = "Read")

class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    panel = Column(String(250))
    depth_mean = Column(Float)
    faf_mean = Column(Float)
    faf_sd = Column(Float)
    faf_cv = Column(Float)
    num_runs = Column(Integer)
    snp_id = Column(Integer, ForeignKey("snp.id"))
    snp = relationship(SNP, backref = "Stats" )
    
 
    
Base.metadata.create_all()
session.close()