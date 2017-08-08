#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 15:17:53 2017

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

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

Base = declarative_base()
#engine = create_engine('mysql+pymysql://root@localhost:3306/cpd_all', echo=False)
engine = create_engine('sqlite:///CPD.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def make_plot(x, df, cutoffs, p):
    #load bins
    lowers = []
    uppers = []
    cvs = []
    for i in range(len(cutoffs)-1):
        u = cutoffs[i+1]
        uppers.append(u)
        l = cutoffs[i]
        lowers.append(l)
        subset = df.loc[(df[x]<= u) & (df[x] > l), :]
        c = subset['faf_cv']
        cvs.append(c)
    # load traces
    data = []
    for i in range(len(cutoffs)-1):
        trace = go.Box(
                    y = cvs[i],
                    name = "{} - {}".format(lowers[i], uppers[i]),
                    boxpoints = 'all')
        data.append(trace)
        
        # plot details
    xlab = dict(title = x)
    ylab = dict(title = 'CV of FAF')
    layout = go.Layout(title = p, xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=data,layout=layout)
    plot_URL = py.plot(fig, filename = p +  ' ' + x, fileopt= 'overwrite',
                       sharing = 'secret', auto_open = False)
    return
# setup 
panels = ['all'] 
for i in session.query(Read.panel).distinct():
    panels.append(i.panel)

# define bins
faf_cutoffs = np.linspace(0.0,1.0, num = 6).tolist()
fdp_cutoffs = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 
               100000, 1000000]
   
for p in panels:
    q = session.query(Stats).filter_by(panel = p)
    df = pd.read_sql_query(q.statement, engine)
    make_plot('faf_mean', df, faf_cutoffs, p)
    make_plot('fdp_mean', df, fdp_cutoffs, p)

session.close()



