# The number of sub-populations is important for scalability 
# This script plots boxes of the time requiered to complete an experiment
# for different number of workers and dimensions. 

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from itertools import groupby
from operator import itemgetter



# 1, 2, 4, 8 workers
# For now these files are fixed 
file_list_5m =  [
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\1w05mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\4w05mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\8w05mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\16w05mEC2.csv',
]


file_list_10m = [r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\1w10mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\4w10mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\8w10mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\16w10mEC2.csv',
]


file_list_20m =  [
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\1w20mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\4w20mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\8w20mEC2.csv',
                r'C:\Users\mario\EC2_experiment_data\ExperimentosAWS-2048\16w20mEC2.csv',
]


def get_data_frame(file):
    data = pd.read_csv(file, header=None, names=['dim', 'instance', 'time_stamp', 'num_evals'] )
    return data


resample_step = {10:'30S',20:'60S'}
worker_labels = [ "1w",  "4w",  "8w", "16w"]

pop_size = {10:'140',20:'200' }

def get_box_dimensions(file_list):
    box_dimensions = { 10:[], 20:[]}
    for worker_index , file in enumerate(file_list):
        df = get_data_frame(file)
        df.time_stamp = df.time_stamp.apply(datetime.fromtimestamp)  
        df.time_stamp = df.time_stamp.apply(pd.to_datetime)
        for dim_index, (name, dim_group) in enumerate (df.groupby("dim")):
                dim_instance = dim_group.groupby("instance").agg({'time_stamp':[np.min, np.max]})
                time_diff_raw = dim_instance.time_stamp.amax-dim_instance.time_stamp.amin
                box_dimensions[name].append(list(map(lambda x: x.total_seconds(), time_diff_raw  )  ))
    return box_dimensions

#sns.set(style="darkgrid", palette="muted", color_codes=True)
# f, axes = plt.subplots(2, 6)

dimension_list = [ 10,  20]
f, axes = plt.subplots(len(dimension_list) , 3,  sharey='row')

def plot_as_row(row, box_dimensions):
    for index , dim in enumerate(dimension_list):
        ax = axes[row, index]
        ax.grid(True) 
        if row == 0:
            ax.set_title("{0}D ({1})".format(dim, pop_size[dim]))
        ax.boxplot(box_dimensions[dim], sym='',  labels=worker_labels)
        if index == 0:
            ax.set_ylabel("seconds per instance" )
        #if row == 1:
        #    ax.set_xlabel("pop size: {0}".format(pop_size[dim]) )

def plot_as_column(col, box_dimensions):
    for index , dim in enumerate(dimension_list):
        ax = axes[index, col]
        ax.grid(True) 
        if col == 0:
            ax.set_title("{0}D ({1})".format(dim, pop_size[dim]))
        ax.boxplot(box_dimensions[dim], sym='',  labels=worker_labels)
        if index == 0:
            ax.set_ylabel("seconds per instance" )
        

plot_as_column(0, get_box_dimensions(file_list_5m))
plot_as_column(1, get_box_dimensions(file_list_10m))
plot_as_column(2, get_box_dimensions(file_list_20m))


plt.subplots_adjust(left=0.08, bottom=0.11, right=0.90, top=0.88, wspace=0.39, hspace=0.5)
plt.show()
