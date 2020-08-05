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


resample_step = {10:'30S',20:'60S' }
worker_labels = [ "1w",  "4w",  "8w", "16w"]
population_label = ["5 populations", "10 populations", "20 populations",]
pop_size = {10:'140',20:'200' }

def get_box_dimensions(file_list):
    box_dimensions = {10:[], 20:[]}
    for worker_index , file in enumerate(file_list):
        df = get_data_frame(file)
        df.time_stamp = df.time_stamp.apply(datetime.fromtimestamp)
        df.time_stamp = df.time_stamp.apply(pd.to_datetime)
        for dim_index, (name, dim_group) in enumerate (df.groupby("dim")):
                dim_instance = dim_group.groupby("instance").agg({'time_stamp':[np.min, np.max],'num_evals':np.sum})
                dim_instance.columns = dim_instance.columns.droplevel(level=0)

                num_evals = dim_instance['sum']
                time_diff_raw = dim_instance.amax-dim_instance.amin
                time_diff_total = list(map(lambda x: x.total_seconds(), time_diff_raw))

                evals_per_second = num_evals/time_diff_total
                box_dimensions[name].append(evals_per_second)
    return box_dimensions


dimension_list = [10,  20]
f, axes = plt.subplots(len(dimension_list) , ncols=3,  sharey='row')


def plot_as_column(col, box_dimensions):
    for index , dim in enumerate(dimension_list):
        ax = axes[index, col]
        ax.grid(True) 
        if index == 0:
            ax.set_title(population_label[col], fontsize=9)
            #ax.set_title("{0}D ({1})".format(dim, pop_size[dim]), fontsize=9)
        ax.boxplot(box_dimensions[dim], sym='',  labels=worker_labels)
        #if col == 0:
        #    ax.set_ylabel(r"#FE/s" , fontsize=9)

def to_csv(data, file_name):
    for d in dimension_list:
        for i, worker in enumerate(worker_labels):
            df = pd.DataFrame(data[d][i])
            df['worker'] = worker
            df['dim'] = str(d)
            print(df.columns)
            df.to_csv(file_name, mode = 'a', header=False, columns=['dim','worker','sum'])

to_csv(get_box_dimensions(file_list_5m), '../5m.csv')
to_csv(get_box_dimensions(file_list_10m), '../10m.csv')
to_csv(get_box_dimensions(file_list_10m), '../20m.csv')





plot_as_column(0, get_box_dimensions(file_list_5m))
plot_as_column(1, get_box_dimensions(file_list_10m))
plot_as_column(2, get_box_dimensions(file_list_20m))
plt.show()
