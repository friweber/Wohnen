# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 12:19:34 2023

@author: fcweb
"""
import pandas as pd
import matplotlib.pyplot as plt
import functions
import numpy as np

#%% This function creates a plot where in the header the question is shown
# Than all subheaders are created from the responses corresponding to sub
# The mean value for all sub is shown

def position_plot_single(head, sub, response, data_var, data_val, data_quest):
    header_plot = data_quest["VAR"][head]
    sub_header_plot = data_quest["VAR"][sub]
    
    
    # Plotting the lines and markers
    plt.figure(figsize=(8, 8*0.68))
    for i, resp in enumerate(response):
        questions = functions.condition2(data_var, "MEANING", "RESPONSE", resp, "VAR", sub_header_plot)[0]
        awnser = functions.condition2(data_var, "MEANING", "RESPONSE", -9, "VAR", header_plot, False)
        range_vals = functions.condition2(data_var, "RESPONSE", "RESPONSE", -9, "VAR", header_plot, False)
        plt.plot([range_vals[0], range_vals[-1]], [i, i], color='black')  # Line spanning from yes to no
        plt.plot([range_vals[0], range_vals[0]], [i+0.05, i-0.05], color='black')
        plt.plot([range_vals[-1], range_vals[-1]], [i+0.05, i-0.05], color='black')
        plt.text(range_vals[0], i+0.3, questions, ha='left', va='center', weight='bold')
        plt.text(range_vals[0]-(range_vals[-1]-range_vals[0])*0.05, i, awnser[0], ha='right', va='center')
        plt.text(range_vals[-1]+(range_vals[-1]-range_vals[0])*0.05, i, awnser[-1], ha='left', va='center')
        value = np.nanmean(functions.condition(data_val, header_plot, sub_header_plot, i+1))
        plt.scatter(value, i, s=150, color="k", marker='o', alpha = 1)  # Dot for the average
    
    # Add a vertical line at position 3
    plt.axvline(x=(range_vals[-1]+range_vals[0])/2, color='gray', linestyle='--', alpha = 0.4)
    
    # Hide the box
    plt.box(on=None)
    
    # Set x-axis labels
    plt.xticks([])
    plt.yticks([])
    title = functions.condition(data_quest, "QUESTION", "VAR", header_plot)[0]
    plt.title(title, weight='bold')# Show plot
    plt.tight_layout()

#%%
#%%
def plot_hist(quest, data_var, data_val, data_quest, includes = None):
    title = data_quest["LABEL"][quest]
    header = data_quest["VAR"][quest]
    bin_labels = functions.condition2(data_var, "MEANING", "RESPONSE", -9, "VAR", header, False)
    
    data = functions.condition_int(data_val, header, header, -9, False)
    
    if includes:
        new_data = []
        new_bin_labels = []
        for include in includes:
            new_data.extend(data[data == include])
            new_bin_labels.append(bin_labels[include-1])
        data = new_data
        bin_labels = new_bin_labels
    

    
    
    # Calculate the bin positions and widths
    bin_positions = np.arange(len(bin_labels) + 1) +0.5  # Center bins at integers
    
    # Create histogram with custom bin positions
    plt.hist(data, bins=bin_positions, edgecolor='black', align='mid', density = "True")
    # Get current y-axis ticks
    y_vals = plt.gca().get_yticks()
    
    counts, bins = np.histogram(data, bins=bin_positions)
    total_counts = np.sum(counts)
    percentages = [(counter / total_counts) * 100 for counter in counts]
    # Convert y-axis ticks to percentages
    y_labels = [str(int(y * 100)) for y in y_vals]
    
    
    # Set the y-axis labels to show percentages
    plt.gca().set_yticklabels(y_labels)
    # Set x-axis tick positions and labels
    tick_positions = np.linspace(1, len(bin_labels), len(bin_labels))  # Tick positions at midpoints
    plt.xticks(tick_positions, bin_labels, rotation=45, ha='right', fontsize='small')
    
    for i, pos in enumerate(bin_positions[:-1]):
        plt.text(pos+0.25, (percentages[i]+2.3)/100, str(np.round(percentages[i],1)) + "%", color='k', va='center')
    plt.ylabel('Anteil %')
    plt.title(title,wrap=True)
    plt.ylim(0,(np.max(percentages)+5)/100)
    plt.tight_layout()