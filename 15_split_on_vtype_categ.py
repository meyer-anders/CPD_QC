#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 20:12:55 2017

@author: Anders
"""

import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from functions import make_box
import numpy as np


print('making overall bar graph')

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
        df.fdp_cv = df.fdp_std/df.fdp_mean
        trace = go.Bar(x = ['Mean CV of FAF', 'Mean FAF', 'Mean CV of FDP'],
               y = [df.faf_cv.mean(), df.faf_mean.mean(), df.fdp_cv.mean()],
               name = '{} {}'.format(panel_name, panel_version),
               yaxis = 'y1')
        traces.append(trace)

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
layout = go.Layout(barmode='group')
fig = go.Figure(data=traces, layout=layout)
py.image.save_as(fig, filename='overall.png', scale = 3)


        
