#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:20:43 2017

@author: Anders
"""

#==============================================================================
# FILTER INPUT
filters = {'num_run_min' : 0,
           'faf_filter_max' : 1.0,
           'faf_filter_min' : 0.0}

filter_tag = None
#==============================================================================

import os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import math
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import create_engine, exists, func
from cpd_db_setup2 import SNP, Read, Stats
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

Base = declarative_base()
engine = create_engine('sqlite:///cpd2.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def apply_filters(df, f):
    df = df[df['num_runs']>f['num_run_min']]
    df = df[df['faf_mean']<f['faf_filter_max']]
    df = df[df['faf_mean']>f['faf_filter_min']]
    return df

def make_plot (data, panel, x, y, split = None, filter_tag= None,
               categoryorder = None, categoryarray = None):    
    xlab = dict(title = x)
    if not categoryorder == None:
        xlab['categoryorder'] = categoryorder
        xlab['categoryarray'] = categoryarray
    ylab = dict(title = y)
    title = panel + '_' + ylab['title'] + '_by_' + xlab['title']
    if not split == None:
        title = title + '_split_by_' + split
    if not filter_tag == None:
        title = title + '_filter_on_' + filter_tag
    layout = go.Layout(title = title, xaxis = xlab, yaxis = ylab)
    fig = go.Figure(data=data,layout=layout)
    return py.plot(fig, filename = title, fileopt= 'overwrite',
                   sharing = 'secret', auto_open = False)

# Setup, data import

panels = []
for i in session.query(Stats.panel).distinct():
    panels.append(i.panel)
snps = session.query(SNP).all()
stats = pd.read_sql_query(session.query(Stats).statement, engine)
n = len(stats)
for i in range(n):
    for snp in snps:
        if snp.id == stats.snp_id.iloc[i]:
            stats.loc[i, 'dbsnp'] = str(snp.dbsnp)
            stats.loc[i, 'gene'] = snp.gene
            stats.loc[i, 'effect'] = snp.effect
            stats.loc[i, 'categ'] = snp.categ
            stats.loc[i, 'var_type'] = snp.var_type

# Loop over panels to make all charts for ech panel
for p in panels:
    DF = stats[stats['panel']==p]
    df = apply_filters(DF, filters)

    # Overall
    trace = go.Scatter(
        x = df.depth_mean,
        y = df.faf_cv,
        mode = 'markers',
        hovertext = df.gene + ", dbsnp " + df.dbsnp)
    data = [trace]
    plot_url = make_plot(data = data,
             panel = p,
             x='read_depth',
             y='cv',
             filter_tag = filter_tag)
   
    # Split by category, effect, var_type
    df.categ.fillna('None', inplace = True)
    splits = ['categ', 'effect', 'var_type']
    for i in splits:
        l = []
        for x in df[i].unique():
            temp_df = df[df[i]==x]
            trace = go.Scatter(x = temp_df.depth_mean,
                               y = temp_df.faf_cv,
                               name = x,
                               mode = 'markers',
                               hovertext = df.gene + ", dbsnp " + df.dbsnp)
            l.append(trace)    
        plot_url = make_plot(data = l,
                     panel = p,
                     x='read_depth',
                     y='cv',
                     split = i,
                     filter_tag = filter_tag)
    
    # Split by FAF
    l = []
    temp_df = df[df['faf_mean'] < 0.4]
    trace = go.Scatter(x = temp_df.depth_mean,
                       y = temp_df.faf_cv,
                       name = "FAF < 40%",
                       mode = 'markers',
                       hovertext = df.gene + ", dbsnp " + df.dbsnp)
    l.append(trace)
    temp_df = df[df['faf_mean'] > 0.4]
    temp_df = temp_df[temp_df['faf_mean']<0.6]
    trace = go.Scatter(x = temp_df.depth_mean,
                       y = temp_df.faf_cv,
                       name = "FAF 40-60%",
                       mode = 'markers',
                       hovertext = df.gene + ", dbsnp " + df.dbsnp)
    l.append(trace)
    temp_df = df[df['faf_mean'] > 0.6]
    trace = go.Scatter(x = temp_df.depth_mean,
                       y = temp_df.faf_cv,
                       name = "FAF > 60%",
                       mode = 'markers',
                       hovertext = df.gene + ", dbsnp " + df.dbsnp)
    l.append(trace)
    plot_url = make_plot(data = l,
                         panel = p,
                         x='read_depth',
                         y='cv',
                         split = 'faf',
                         filter_tag = filter_tag)

    # Split by gene   
    genes = list(df['gene'].unique())
    gene_df = pd.DataFrame(index = genes)
    for g in genes:
        temp_df = df[df['gene']==g]
        gene_df.loc[g, 'faf_cv'] = temp_df.faf_cv.mean()
    gene_df = gene_df.sort_values('faf_cv', ascending = False)
    genes = gene_df.index.tolist()
    l = []
    for g in genes:
        temp_df = df[df['gene']==g]
        trace = go.Box(y = temp_df.faf_cv,
                       name = g,
                       boxpoints = 'suspectedoutliers')
        l.append(trace)
    plot_url = make_plot(data = l,
                     panel = p,
                     x='genes',
                     y='cv',
                     filter_tag = filter_tag,
                     categoryorder = "array", categoryarray = genes)

session.close()





 