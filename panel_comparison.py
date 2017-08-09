#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:30:04 2017

@author: Anders
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import math
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func, and_
from cpd_db_setup2 import Variant, Read, Stats
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from scipy import stats

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

Base = declarative_base()
#engine = create_engine('mysql+pymysql://root@localhost:3306/cpd_all', echo=False)
engine = create_engine('sqlite:///CPD.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#panels = ['TSCA','bPPP']
p = 'bPPP'
'''
- get variants in p
- get variants in solid
- ?inner join to get variants in both
- 

'''
data = pd.DataFrame(columns = ['var_id', 'Solid', p])

a1 = aliased(Stats)
a2 = aliased(Stats)

v_in_both = session.query(a1.var_id, a2.var_id).\
                        filter(and_(a1.panel=='Solid', a2.panel ==p)).\
                        filter(a1.var_id == a2.var_id).all()

for v in v_in_both:
    faf_data = session.query(a1.faf_mean, a2.faf_mean).\
                            filter(and_(a1.panel=='Solid', a1.var_id == v[0])).\
                            filter(and_(a2.panel==p, a2.var_id == v[0])).\
                            filter(a1.sample == a2.sample).one_or_none()
    if faf_data != None:
        new_stat = {'var_id': v[0],
                    'Solid' : faf_data[0],
                    p : faf_data[1]}
        data = data.append(new_stat, ignore_index = True)

