#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 16:04:11 2017

@author: Anders
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'functions',
  ext_modules = cythonize("functions.pyx"),
)