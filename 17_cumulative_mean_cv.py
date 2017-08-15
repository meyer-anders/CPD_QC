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
from functions import plot_cumulative_cv


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
        for c in cols:
            this_panel = []
            for s in sides:
                trace = plot_cumulative_cv(df, c, s)
                trace_dict[(c,s)].append(trace)
                trace.name = s
                this_panel.append(trace)
                
            os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
            xlab = dict(title = c)
            ylab = dict(title = 'Average mean FAF CV')
            layout = go.Layout(title = 'Average mean FAF CV for{} {}'.\
                               format(panel_name, panel_version), 
                               xaxis = xlab, yaxis = ylab)
            fig = go.Figure(data=this_panel, layout=layout)
            try:
                py.image.save_as(fig, filename='cumulative_CV_{}_{}_{}.png'.\
                                 format(c, panel_name, panel_version), scale = 3)
            except:
                plotly.offline.plot(fig)
                input("Press Enter to continue...")
        

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
for k, v in trace_dict.items():
    xlab = dict(title = k[0])
    ylab = dict(title = 'Average mean FAF CV to the {}'.format(k[1]))
    layout = go.Layout(title = 'Average mean FAF CV to the {}'.format(k[1]), 
                       xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=v, layout=layout)
    try:
        py.image.save_as(fig, filename='{}_{}_all_panels.png'.\
                         format(k[0], k[1]), scale = 3)
    except:
        plotly.offline.plot(fig)