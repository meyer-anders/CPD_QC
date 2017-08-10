#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:30:04 2017

@author: Anders

to do:
    - add annotation to line
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

data = pd.DataFrame(columns = ['var_id', 'Solid', p])

a1 = aliased(Stats)
a2 = aliased(Stats)
traces = []
for p in panels:
    faf_data = session.query(a1, a2).filter(and_(a1.panel=='Solid', a2.panel == p)).\
                                filter(a1.var_id == a2.var_id).\
                                filter(a1.sample == a2.sample).all()
    for f in faf_data:
        new_stat = {'var_id': f[0].var.gene,
                    'Solid' : f[0].faf_mean,
                    p : f[1].faf_mean}
        data = data.append(new_stat, ignore_index = True)
    # plot data
    x = data['Solid']
    y = data[p]
    trace = go.Scatter(
                  x = x,
                  y = y,
                  mode='markers',
                  name= p)
    traces.append(trace)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    line = slope*x+intercept
    trace = go.Scatter(
            x = x,
            y = line,
            mode = 'lines',
            hoverinfo = 'none',
            name = '{} fit'.format(p))
    traces.append(trace)

xlab = dict(title = 'Mean FAF on Solid panel')
ylab = dict(title = 'Mean FAF')
title = 'Comparison of Panels'
layout = go.Layout(title = title , xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces,layout=layout)
plot_URL = py.plot(fig, filename = title, fileopt= 'overwrite',
                   sharing = 'secret', auto_open = False)

