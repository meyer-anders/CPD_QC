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
import pymysql

#engine = create_engine('sqlite:///cpd2.db')
engine = create_engine('mysql+pymysql://root@localhost:3306/cpd2', echo=False)
Base = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
 



class Variant(Base):
    __tablename__ = "variant"
    id = Column(Integer, primary_key=True)
    position = Column(String(250))
    nucleotide = Column(String(250))
    gene = Column(String(250))
    chromosome = Column(String(250))
    effect = Column(String(250))
    var_type = Column(String(250))
    categ = Column(String(250))

class Read(Base):
    __tablename__ = "read"
    id = Column(Integer, primary_key = True)
    fdp = Column(Integer)
    frd = Column(Integer)
    fad = Column(Integer)
    faf = Column(Float)
    panel = Column(String(250))
    sample = Column(String(250))
    run = Column(String(250))
    quality = Column(Float)
    var_id = Column(Integer, ForeignKey("variant.id"))
    var = relationship(Variant, backref = "Read")
    

class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    panel = Column(String(250))
    fdp_mean = Column(Float)
    faf_mean = Column(Float)
    faf_sd = Column(Float)
    faf_cv = Column(Float)
    num_runs = Column(Integer)
    var_id = Column(Integer, ForeignKey("variant.id"))
    var = relationship(Variant, backref = "Stats" )
    
 
    
Base.metadata.create_all()
session.close()