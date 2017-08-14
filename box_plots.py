#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 00:25:07 2017

@author: Anders
"""

import os
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from functions import make_box
import numpy as np

print('making box plots')

plotly.tools.set_credentials_file(username='andmeyer', 
                                  api_key='Vx28T2v1QEhiEHqujoc6')


faf_cutoffs = np.linspace(0.0,1.0, num = 6).tolist()
fdp_cutoffs = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 50000, 
               100000, 1000000]


os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
for file in os.listdir():
    if file.endswith(".csv"):
        os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Stats')
        df = pd.read_csv(file)
        panel_name = df.panel_name[0]
        panel_version = df.panel_version[0]
        print(panel_name, panel_version)
        make_box('faf_mean', df, faf_cutoffs, panel_name, panel_version)
        make_box('fdp_mean', df, fdp_cutoffs, panel_name, panel_version)

    


