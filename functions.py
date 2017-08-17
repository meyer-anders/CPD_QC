#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 15:38:45 2017

@author: Anders
"""
import os
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from scipy import stats


def concat_data(directory, fields):
    '''
    Reads in all data files in the directory and combines them along the fields
    and with the data types specified in 'fields'. Returns concatenated DF.
    Crudely handles errors.
    '''
    
    os.chdir(directory)
    dfs = []
    for file in os.listdir():
        try:
            if file.endswith(".csv"):
                dfs.append(pd.read_csv(file, dtype = fields, usecols = fields.keys()))
            if file.endswith(".tab"):
                dfs.append(pd.read_table(file, dtype = fields, usecols = fields.keys()))
            if file.endswith(".xls") or file.endswith(".xlsx"):
                dfs.append(pd.read_excel(file, converters = fields, usecols = fields.keys()))
        except:
            print('error loading {}'.format(file))
    return pd.concat(dfs, ignore_index = True)
        
        
def plot_cumulative_cv(df, col, side):
    panel_name = df.panel_name[0]
    panel_version = df.panel_version[0]
    df = df.dropna(subset =['faf_cv', col]).\
        sort_values(by = col, ascending = True).\
        reset_index(drop = True)
    df['cum_avg'] = np.nan
    df = df[[col, 'faf_cv', 'cum_avg']]
    nrows = len(df)
    if side == 'right':
        for i in range(nrows):
            df.loc[i, 'cum_avg'] = df.faf_cv[i:].mean()
    else:
        for i in range(nrows):
            df.loc[i, 'cum_avg'] = df.faf_cv[:i].mean()
    trace = go.Scatter(x = df[col],
                       y = df.cum_avg,
                       mode = 'line',
                       name = '{} {}'.format(panel_name, panel_version))
    return trace

def get_overlap(a, b):
    os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
    A = pd.read_csv('{}_stats.csv'.format(a))
    B = pd.read_csv('{}_stats.csv'.format(b))
    
    
    sjoined = A.merge(B, how ='inner', on = 'sample').\
                    drop_duplicates(subset = 'sample')
    vjoined = A.merge(B, how ='inner', on = 'var_id').\
                    drop_duplicates(subset = 'var_id')
    bjoined = A.merge(B, how ='inner', on = ['sample', 'var_id'])
    panel_line = pd.Series({'panel_A':a, 'panel_B' : b, 
                            'var_overlap': len(vjoined), 
                            'sample_overlap' :len(sjoined),
                            'both_overlap' : len(bjoined)})
    return panel_line

def compare(comparisons):
    panel_summary = pd.DataFrame(columns = ['panel_A', 'panel_B', 'var_overlap', 
                                        'sample_overlap', 'both_overlap', ])
    for p in comparisons:
        panel_summary = panel_summary.append(
                get_overlap(p[0], p[1]), ignore_index = True)
    
    return panel_summary



def parse_sample_name(df): 
    names = df.seq_name.copy().drop_duplicates()    
    dicts = []
    for r in names:
        split = r.split("-")
        d = {'seq_name' : r,
            'sample': str(split[0]),
             'chemistry' : str(split[-8]),
             'chem_number' : int(str(split[-7])),
             'pal' : int(str(split[-3])),
             'seq' : int(str(split[-1])),
             'repeat' : (str(split[1]) == 'A'),
             'year' : int(split[0][4:6]),
             'acc_num' : int(split[0][6:])}
        dicts.append(d)        
    
    temp_df = pd.DataFrame()
    temp_df = temp_df.from_dict(dicts)
    return df.merge(temp_df, how = 'left', on = 'seq_name')
        
        
    
    
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
                       xaxis = xlab, yaxis = ylab, showlegend=False)
    fig = go.Figure(data=data,layout=layout)

    py.image.save_as(fig, filename=filename, scale = 3)
    return

def make_correlation(xvar, yvar):
    os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
    X = pd.read_csv('{}_stats.csv'.format(xvar))
    Y = pd.read_csv('{}_stats.csv'.format(yvar))
    
    os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Plots')
    filename = 'Correlation of {} and {}.png'.format(xvar, yvar)
    
    joined = X.merge(Y, how = 'inner', 
                    on = ['var_id', 'sample'])[['var_id','faf_mean_x', 'faf_mean_y']]
    x = joined.faf_mean_x
    y = joined.faf_mean_y

    traces = []
    trace = go.Scatter(
                  x = x,
                  y = y,
                  mode='markers',
                  name= yvar)
    traces.append(trace)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    line = slope*x+intercept
    trace = go.Scatter(
            x = x,
            y = line,
            mode = 'lines',
            hoverinfo = 'none',
            name = '{} fit'.format(yvar))
    traces.append(trace)


    xlab = dict(title = 'Mean FAF on {}'.format(xvar), range = [0,1.1])
    ylab = dict(title = 'Mean FAF on {}'.format(yvar), range = [0,1.1])
    title = 'Comparison of Panels  \nR^2 = {:.2}, Y = {:.2}X + {:.2}'.\
                          format(r_value**2, slope, intercept)
    layout = go.Layout(title = title , xaxis = xlab, yaxis = ylab,
                       showlegend = False)
    fig = go.Figure(data=traces,layout=layout)
    py.image.save_as(fig, filename=filename, scale = 3)
    return

def make_comparisons(comparisons):
    for p in comparisons:
        make_correlation(p[0], p[1])
    return