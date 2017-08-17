#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 21:28:34 2017

@author: Anders
"""

import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from plotly.graph_objs import Box, Layout


print('plotting number of runs')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')

traces = []
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        panel_name = df.panel_name[0]
        panel_version = df.panel_version[0]
        
        trace = go.Box(
                    y = df['faf_count'],
                    name = '{}_{}'.format(panel_name, panel_version),
                    boxpoints = 'all')
        traces.append(trace)

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
xlab = dict(title = 'Panels')
ylab = dict(title = 'Number of Runs')
layout = go.Layout(title = 'Number of Runs by Panel', xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces, layout=layout)
#plotly.offline.plot(fig)
py.image.save_as(fig, filename='num_runs.png', scale = 3)


        
