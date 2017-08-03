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
from colour import Color
plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

Base = declarative_base()
engine = create_engine('mysql+pymysql://root@localhost:3306/cpd2', echo=False)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# input
panel = 'bPPP'
   

# join stats tables with variant info, limit to desired panel
q = session.query(Stats).join(Stats.var)
stats = pd.read_sql_query(q.statement, engine)
df = stats[stats['panel']==panel]

# define bins
num_bins = 20
faf_cutoffs = np.linspace(0.0,1.0, num = num_bins+1).tolist()
fdp_cutoffs = np.linspace(0,stats.fdp.max(), num = num_bins+1).tolist()

# define colors
lime = Color("lime")
colors = list(red.range_to(lime, 20))

# load bins
bins = pd.DataFrame(columns = ['lower', 'upper', 'y', 'mean'])
for i in range(0, num_bins):
    upper = faf_cutoffs[i+1]
    lower = faf_cutoffs[i]
    bins.set_value(i, 'upper', str(upper*100))
    bins.set_value(i, 'lower', str(lower*100))
    subset = df[df['faf']< upper and df['faf']> lower]
    y = subset.faf_cv
    bins.set_value(i, 'y', y)
    bins.set_value(i, 'mean', y.mean())
    
bins.sort('mean', ascending = False, inplace = True)

# load traces
data = []
for i, c in zip(range(num_bins),colors):
    trace = go.Box(
                y = bins.y.iloc[i],
                name = bins.lower.iloc[i] + '-' + bins.upper.iloc[i],
                boxpoints = 'outliers',
                marker = dict(color = c),
                line = dict(color = c))
    data.append(trace)

# plot details
xlab = dict(title = 'Variant Frequency (FAF)')
ylab = dict(title = 'CV of FAF')
title = panel
layout = go.Layout(title = title, xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=data,layout=layout)
plot_URL = py.plot(fig, filename = panel + 'boxplot on FAF', fileopt= 'overwrite',
               sharing = 'secret', auto_open = False)

