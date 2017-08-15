#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 12:59:19 2017

@author: Anders
"""
import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from functions import make_box
import numpy as np


print('splitting by variant type and category')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_exports')
reads = pd.read_csv('reads8.csv')
vtypes= sorted(list(reads.vtype.copy().dropna().drop_duplicates()))
categs= sorted(list(reads.categorization.copy().dropna().drop_duplicates()))

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')


vtraces = []
ctraces = []
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        panel_name = df.panel_name[0]
        panel_version = df.panel_version[0]
        panel = '{}_{}'.format(panel_name, panel_version)
        
        for v in vtypes:
            vtrace = go.Box(
                        y = df.loc[df.vtype == v, 'faf_cv'],
                        name = v,
                        boxpoints = 'outliers')
            vtraces.append(vtrace)
        
        for c in categs:
            ctrace = go.Box(
                        y = df.loc[df.categorization == c, 'faf_cv'],
                        name = c,
                        boxpoints = 'outliers')
            ctraces.append(ctrace)
        
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
        ylab = dict(title = 'Variant types')   
        title = 'Split by variant type'
        layout = go.Layout(title = title , yaxis = ylab)         
        fig = go.Figure(data=vtraces, layout=layout)
        py.image.save_as(fig, filename='{}_split_by_vtype.png'.format(panel),
                         scale = 3)
        
        ylab = dict(title = 'Categorizations')
        title = 'Split by categorizations'
        layout = go.Layout(title = title , yaxis = ylab)         
        fig = go.Figure(data=ctraces, layout=layout)
        py.image.save_as(fig, filename='{}_split_by_categ.png'.format(panel),
                         scale = 3)