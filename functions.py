#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:38:45 2017

@author: Anders
"""
import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from scipy import stats


def parse_sample_name(df):
    df.sample = np.nan
    df.chemistry = np.nan
    df.chem_number = np.nan
    df.pal = np.nan
    df.seq = np.nan
    df.repeat = np.nan
    df.year = np.nan
    df.acc_num = np.nan
    names = df.seq_name.drop_duplicates()
    n = 0
    t = len(names)
    for r in names:
        sample_name = r
        split = sample_name.split("-")
        mask = df.seq_name == sample_name
        d = {'sample': str(split[0]),
             'chemistry' : str(split[-8]),
             'chem_number' : int(str(split[-7])),
             'pal' : int(str(split[-3])),
             'seq' : int(str(split[-1])),
             'repeat' : (str(split[1]) == 'A'),
             'year' : int(split[0][4:6]),
             'acc_num' : int(split[0][6:])}
        for k, v in d.items():
            df.loc[mask, k] = v
        
        n += 1
        if n%500 ==0:print('{} of {} rows parsed'.format(n, t))
    
    
    #drop inapprpriate non-numeric entries
    df['chem_number'] = pd.to_numeric(df['chem_number'], errors = 'coerce').\
                        fillna(0).astype(int)
    return df

def make_box(x, df, cutoffs, panel_name, panel_version):
    #load bins
    filename = '{}_v{}_{}.png'.format(panel_name, panel_version,x)
    os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
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
        if cutoffs[1]<1:
            name = "{:.2} - {:.2}".format(lowers[i], uppers[i])
        else:
            name = "{} - {}".format(lowers[i], uppers[i])
        trace = go.Box(
                    y = cvs[i],
                    name = name,
                    boxpoints = 'all')
        data.append(trace)
        
        # plot details
    xlab = dict(title = x)
    ylab = dict(title = 'CV of FAF')
    layout = go.Layout(title = '{} v{}'.format(panel_name, panel_version), 
                       xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=data,layout=layout)
#    plot_URL = py.plot(fig, filename = p +  ' ' + x, fileopt= 'overwrite',
#                       sharing = 'secret', auto_open = False)
    py.image.save_as(fig, filename=filename, scale = 3)
    return

def make_correlation(compare):
    
    os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
    x_label = compare['x'][0]
    y_label = compare['y'][0]
    filename = 'Correlation of {} and {}.png'.format(x_label, y_label)
    
    joined = compare['x'][1].merge(compare['y'][1], how = 'inner', on = 'var_id')\
                                [['var_id','faf_mean_x', 'faf_mean_y']]
    x = joined.faf_mean_x
    y = joined.faf_mean_y

    traces = []
    trace = go.Scatter(
                  x = x,
                  y = y,
                  mode='markers',
                  name= y_label)
    traces.append(trace)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    line = slope*x+intercept
    trace = go.Scatter(
            x = x,
            y = line,
            mode = 'lines',
            hoverinfo = 'none',
            name = '{} fit'.format(y_label))
    traces.append(trace)

    xlab = dict(title = 'Mean FAF on {}'.format(x_label))
    ylab = dict(title = 'Mean FAF on {}'.format(y_label))
    title = 'Comparison of Panels'
    layout = go.Layout(title = title , xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=traces,layout=layout)
    py.image.save_as(fig, filename=filename, scale = 3)