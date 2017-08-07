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

# input
panel = 'bPPP' 
   

# join stats tables with variant info, limit to desired panel
q = session.query(Stats).join(Stats.var).filter(Stats.panel == panel)
df = pd.read_sql_query(q.statement, engine)
#df = stats[stats['panel']==panel]

# define bins

faf_cutoffs = np.linspace(0.0,1.0, num = 21).tolist()
fdp_cutoffs = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 
               100000, 1000000]

def make_plot(x, cutoffs):
    #load bins
    bins = pd.DataFrame(columns = ['lower', 'upper', 'y'])
    for i in range(0, len(cutoffs)-1):
        upper = cutoffs[i+1]
        lower = cutoffs[i]
        bins.set_value(i, 'upper', str(int(upper*100)))
        bins.set_value(i, 'lower', str(int(lower*100)))
        subset = df[df[x]< upper ]
        subset = subset[subset[x]> lower]
        y = subset.faf_cv
        bins.set_value(i, 'y', y)
    
    # load traces
    data = []
    for i in range(len(cutoffs)-1):
        trace = go.Box(
                    y = bins.y.iloc[i],
                    name = bins.lower.iloc[i] + '-' + bins.upper.iloc[i],
                    boxpoints = 'outliers')
        data.append(trace)
    
    # plot details
    xlab = dict(title = x)
    ylab = dict(title = 'CV of FAF')
    layout = go.Layout(title = panel, xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=data,layout=layout)
    plot_URL = py.plot(fig, filename = panel+  ' ' + x, fileopt= 'overwrite',
                   sharing = 'secret', auto_open = False)
    return

make_plot('faf_mean', faf_cutoffs)
make_plot('fdp_mean', fdp_cutoffs)



