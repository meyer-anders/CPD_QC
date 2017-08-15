#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:15:15 2017

@author: Anders
"""
import os
import pandas as pd
from parse import parse
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


print('plotting simnulations')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Simulations')

traces = []
clin_change = 0.3
for file in os.listdir():
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        str_format = '{}_{}_simulation.csv'
        panel_name, panel_version = parse(str_format, file)
        nrows = len(df)
        trace = go.Scatter(x = pd.Series(range(nrows)),
                        y = df.surviving,
                       mode = 'line',
                       name = '{} {}'.format(panel_name, panel_version))
        traces.append(trace)
 
os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
xlab = dict(title = 'Samples')
ylab = dict(title = 'Percent without {}% change'.format(clin_change*100))
layout = go.Layout(title = 'Simulated Clinical Significance of Variance, n = {}'.\
                   format(nrows), xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces, layout=layout)
py.image.save_as(fig, filename='simulation.png', scale = 3)