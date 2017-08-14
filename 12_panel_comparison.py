#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 08:10:42 2017

@author: Anders
"""


import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from scipy import stats
import os
from functions import make_correlation

print('making panel comparisons')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')


solid1 = pd.read_csv('Solid_v1.0_stats.csv')
solid2 = pd.read_csv('Solid_v2.0_stats.csv')
heme1 = pd.read_csv('Heme_v1.0_stats.csv')
heme3 = pd.read_csv('Heme_v3.0_stats.csv')
ppp = pd.read_csv('PPP_v1.0_stats.csv')

make_correlation({'x': ('Solid_v1.0', solid1),'y': ('Solid_v2.0', solid2)})
make_correlation({'x': ('Solid_v2.0', solid2),'y': ('PPP_v1.0', ppp)})
make_correlation({'x': ('Heme_v1.0', heme1),'y': ('Heme_v3.0', heme3)})