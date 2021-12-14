#!/usr/bin/env python
#You need to have pandas installed:
#pip3 install --user pandas

import_separator = ','
output_separator = ','
other_column_separator = ','
output_filename = 'callsigns_opengd77.csv'

import pandas as pd
import sys

if len(sys.argv) !=2:
    print("Please, provide an ODS contact CSV file")
    sys.exit()

try:
    input_list = pd.read_csv(sys.argv[1], sep = import_separator, index_col = 'ID')
#    input_list.rename(columns={'dashboard':'Callsign', 'volačka':'Details', 'další ID':'other_IDs'}, inplace = True)
    input_list.rename(columns={'dashboard':'Callsign', 'volacka':'Details', 'dalsi ID':'other_IDs'}, inplace = True)

    output_list = input_list[['Callsign', 'Details']].copy()
except:
    print("Please, use the ODS file not containing special Czech characters")
    sys.exit()

other_IDs = input_list[input_list['other_IDs'].notnull()].loc[:,'other_IDs']
#je tam jeden radek s teckou
other_IDs = other_IDs.str.replace('.', ',', regex = False)
for member in map(lambda x: x.split(other_column_separator), other_IDs):
    for ID in member:
        ID = ID.strip()
        if (output_list.index != ID).all():
            callsign = input_list[(input_list['other_IDs'].notnull()) & (input_list['other_IDs'].str.contains(ID))].loc[:,'Callsign'].to_string(header = False, index = False)
            details  = input_list[(input_list['other_IDs'].notnull()) & (input_list['other_IDs'].str.contains(ID))].loc[:,'Details'].to_string(header = False, index = False)
            output_list.loc[ID] = [callsign, details]

output_list.sort_values(by='Callsign', inplace = True)

#output_list.drop_duplicates(inplace = True)

#import csv
#output_list.to_csv('callsigns_opengd77.csv', sep=output_separator, index = True, quoting = csv.QUOTE_ALL)
output_list.to_csv(output_filename, sep=output_separator, index = True)
print("File '",output_filename,"' created", sep='')
