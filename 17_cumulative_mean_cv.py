#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 21:43:11 2017

@author: Anders
"""

import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


print('plotting cumulative cv')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')

# do this as dicts

trace_dict = {}
sides = ['right', 'left']
cols = ['fdp_mean', 'faf_mean']
for s in sides:
    for c in cols:
        trace_dict[(c,s)] = []


for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        panel_name = df.panel_name[0]
        panel_version = df.panel_version[0]

        
        trace_dict = plot_cumulative_cv(df, trace_dict)
        

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
for k, v in trace_dict.items():
xlab = dict(title = 'Panels')
ylab = dict(title = 'Number of Runs')
layout = go.Layout(title = 'Number of Runs by Panel', 
                   xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces, layout=layout)
py.image.save_as(fig, filename='num_runs.png', scale = 3)