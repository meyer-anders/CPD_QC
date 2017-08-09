#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 11:03:33 2017

@author: Anders
"""

How database is created

CAUTION: as of now, all must start with clean tables

1. clean_data.py 
    - loads original CPD exports 
    - drops un-needed columns
    - makes two new DFs: reads and variants
    - drops duplicates from both
    - saves output as 'variants.csv' and 'reads.csv'
    - loads ReportedVariants.tab
    - drops duplicates and un-needed columns
    - writes to 'categ.csv'
    *** will need to alter to enable *adding data to the db later

2. cpd_db_setup2.py
    - creates DB schema

3. load_variants.py
    - loads variants.csv
    - bulk inserts into database
    
4. categorize.py
    - loads categ.csv
    - loops over all variants in DB
    - if variant is in reported variants, assigns categorization 

5. load_reads.py
    - load in all reads from reads.csv
    - loop over reads, find the variant in the db
    - add to list of dicts
    - bulk insert

6. load_stats.py
    - loop over samples and panels (including all panels combined)
    - loop over variants, find all relevant reads
    - calculate stats
    - link to variant
    - add to list of dicts
    - bulk insert for every sample

Plotting

1. box_plots.py
    - for each variant, panel, plot faf_cv vs mean faf and mean fdp

    