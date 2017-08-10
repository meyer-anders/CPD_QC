#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:23:12 2017

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


panels = ['bPPP']
p = 'bPPP'
a1 = aliased(Stats)
a2 = aliased(Stats)

data = pd.DataFrame(columns = ['var_id', 'Solid', p])

#v_in_both = session.query(a1.var_id, a2.var_id).\
#                            filter(and_(a1.panel=='Solid', a2.panel ==p)).\
#                            filter(a1.var_id == a2.var_id).distinct().all()

faf_data = session.query(a1, a2).filter(and_(a1.panel=='Solid', a2.panel == p)).\
                                filter(a1.var_id == a2.var_id).\
                                filter(a1.sample == a2.sample).all()