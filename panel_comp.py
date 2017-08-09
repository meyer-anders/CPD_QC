#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 15:04:01 2017

@author: Anders
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import math
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
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
#panels = ['TSCA','bPPP']


traces = []
for p in panels:
    # load a df, 'data', that plots faf_mean on a panel vs the same on the solid panel
    data = pd.DataFrame(columns = ['var_id', 'Solid', p])
    vars_in_panel = session.query(Stats).filter_by(panel = p).all()
    for v in vars_in_panel:        
        q = session.query(Stats).filter(Stats.var_id == v.var_id, 
                         Stats.panel == 'Solid')
        if session.query(q.exists()).scalar():
            samples = q.distinct(Stats.sample).all()
            q = session.query(Stats).filter(Stats.var_id == v.var_id)
            df = pd.read_sql_query(q.statement, engine)
            for s in samples:
                var = df.loc[df.sample == s.sample, :]
                var = var.loc[(var.panel == p) | (var.panel == 'Solid'), :]
                new_stat = {'var_id': var.var_id[0],
                            'Solid' : var.loc[var.panel == 'Solid', 'faf_mean'],
                            p : var.loc[var.panel == p, 'faf_mean']}
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

# plot details
xlab = dict(title = 'Mean FAF on Solid panel')
ylab = dict(title = 'Mean FAF')
title = 'Comparison of Panels'
layout = go.Layout(title = title , xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces,layout=layout)
plot_URL = py.plot(fig, filename = title, fileopt= 'overwrite',
                   sharing = 'secret', auto_open = False)
    
            
        
    
