#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 11:03:33 2017

@author: Anders
"""

How database is created

CAUTION: as of now, process must start with clean tables

Cleaning read data:
    _ get_reads 1
    1 drop_failed_runs 2
    2 parse_runs 3
    3 assign_panel_names 4
    4 drop_panels 5
    5 revise_panel_versions 6
    _ get_categories _
    6 assign_categories 7
    7 set_keys 8

Stats:
    do_stats
    
15. plot_cv_vs_faf
16. plot_cv_vs_fdp
17. plot_new_vs_old
18. plot_ppp_vs_solid(v2?)
29. plot_v_over_time
 



1. collate_data.py 
    - loads original CPD exports 
    - drops un-needed columns
    - makes new DFs: reads and variants
    - drops duplicates from both
    - saves output as 'variants.csv' and 'reads.csv'
    - loads ReportedVariants.tab
    - drops duplicates and un-needed columns
    - writes to 'categ.csv'
    *** will need to alter to enable *adding data to the db later

2. clean_data.py
    - loads reads.csv and failed_seq...tab
    - removes failed runs from reads
    - looks for sequencing names with 'A' which are repeats
        - if any names are the same but without the 'A', flags them as
            potential failed runs
    - look in failed_runs for panel names
        - take TSCA/etc + following number ('chemistry' + 'chem_number) and
            correlate with the official panel name
        - adds this panel name to reads
        
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

    