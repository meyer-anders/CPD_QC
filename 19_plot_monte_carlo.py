#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 11:15:15 2017

@author: Anders
"""

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
traces = []
for k, v in sample_dict.items():

    trace = go.Scatter(x = pd.Series(range(nrows)),
                        y = df.surviving,
                       mode = 'line',
                       name = '{} {}'.format(k[0], k[1]))
    traces.append(trace)
    
xlab = dict(title = 'Samples')
ylab = dict(title = 'Percent without {}% change'.format(clin_change*100))
layout = go.Layout(title = 'Simulated Clinical Significance of Variance, n = {}'.\
                   format(total), xaxis = xlab, yaxis = ylab)
fig = go.Figure(data=traces, layout=layout)
py.image.save_as(fig, filename='simulation.png.', scale = 3)