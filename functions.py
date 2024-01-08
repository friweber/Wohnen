# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 11:54:38 2023

@author: fcweb
"""

import pandas as pd
import numpy as np

def condition(df, header, header_con, condition, equal = True):
    if equal == True:
        filtered_meanings = df.loc[df[header_con] == condition, header].to_numpy()
    else:
        filtered_meanings = df.loc[df[header_con] != condition, header].to_numpy()
    return(filtered_meanings)

def condition_int(df, header, header_con, condition, equal=True):
    if equal:
        filtered_values = df.loc[df[header_con] == condition, header]
    else:
        filtered_values = df.loc[df[header_con] != condition, header]

    # Convert to numeric and replace non-convertible strings with NaN
    filtered_values = pd.to_numeric(filtered_values, errors='coerce')

    # Filter out NaN values and convert to int
    filtered_integers = filtered_values[~np.isnan(filtered_values)].astype(int).to_numpy()
    return filtered_integers

def condition2_int(df, header, header_con, condition, header_con2, condition2, equal=True):
    if equal:
        filtered_data = df[(df[header_con] == condition) & (df[header_con2] == condition2)][header].to_numpy()
    else:
        filtered_data = df[(df[header_con] != condition) & (df[header_con2] == condition2)][header].to_numpy()
    filtered_values = pd.to_numeric(filtered_data, errors='coerce')

    # Filter out NaN values and convert to int
    filtered_integers = filtered_values[~np.isnan(filtered_values)].astype(int).to_numpy()
    return filtered_integers

def condition2(df, header, header_con, condition, header_con2, condition2, equal=True):
    if equal:
        filtered_data = df[(df[header_con] == condition) & (df[header_con2] == condition2)][header].to_numpy()
    else:
        filtered_data = df[(df[header_con] != condition) & (df[header_con2] == condition2)][header].to_numpy()
    
    return filtered_data