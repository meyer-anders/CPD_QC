import pandas as pd
import os
import numpy as np
from functions import parse_sample_name

os.chdir('/Users/Anders/Dropbox/Projects/CPD_QC/sql2/Data_imports')
'''
SEQUENCING DATA
'''
fields = {'Pos': float, 'Alt': str, 'Gene_name': str, 'Chrom_without_chr': str,
          'Effect': str, 'VariantType': str, 'FDP': float, 'FRD': float, 
          'FAD': float,'Sample Sequencing Name': str}


#original_data = pd.read_excel("validation_full.xlsx", converters = fields, usecols = fields.keys())
#
#dfs = [original_data]
#
##combine data into one df
#final = pd.DataFrame()
#for df in dfs:
#   final = final.append(df, ignore_index = True)
#
#final = final.dropna(subset = ['Pos', 'Chrom_without_chr'])
#
##drop duplicates
#reads = final[['Pos', 'Alt', 'Chrom_without_chr', 'FDP', 'FRD', 'FAD',
#               'Sample Sequencing Name']]
#reads = reads.drop_duplicates(subset = ['Pos', 'Alt', 'Chrom_without_chr', 
#                                        'Sample Sequencing Name'])
#reads = reads.dropna(subset = ['FDP', 'FAD', 'FRD'])
#reads = parse_sample_name(reads)

failed_runs = pd.read_table("failed seq QC data.tab", 
                            usecols = ['Sample Sequencing Name', 'Panel_name'])
failed_runs = failed_runs.dropna(subset = ['Sample Sequencing Name'])
failed_runs = parse_sample_name(failed_runs).\
    loc[:,['chemistry', 'chem_number', 'Panel_name']].drop_duplicates()