#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 08:10:42 2017

@author: Anders
"""
from functions import make_comparisons

print('making panel comparisons')

comparisons = [('Solid_v1.0', 'PPP_v1.0'),
               ('Solid_v2.0', 'PPP_v1.0'),
               ('Heme_v1.0', 'Heme_v2.0'),
               ('Heme_v1.0', 'Heme_v3.0'),
               ('Heme_v2.0', 'Heme_v3.0')]

make_comparisons(comparisons)
