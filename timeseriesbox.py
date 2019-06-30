


import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from itertools import groupby
from operator import itemgetter



# 1, 2, 4, 8 workers
file_list = [r'D:\exp_data\1561526317_1w\swarm_ea_1561526317.json', 
             r'D:\exp_data\1561558363_2w\swarm_ea_1561558363.json',
             r'D:\exp_data\1561750813\swarm_ea_1561750813.json', 
             r'D:\exp_data\1561757026\swarm_ea_1561757026.json'
         #    r'D:\exp_data\1561521129_4w\swarm_ea_1561521129.json',
         #    r'D:\exp_data\1561516494_8w\swarm_ea_1561516494.json'
            ]

def get_data_frame(file):
    data = pd.read_json(file, low_memory=False )
    data.drop([ 'alg_params','evals', 'algorithm', 'best_score', 'experiment_id', 
    'message_counter', 'message_id', 'params', 'worker_id'], axis = 1 )
    data.time_stamp = data.time_stamp.apply(pd.to_datetime)
    return data

labels = ['ts','n','dim','instance','best_score','fopt']


#sns.despine(left=True)
resample_step = {2:'2S', 3:'5S',5:'10S',10:'30S',20:'60S',40:'100S' }
worker_labels = ["1w", "2w", "4w", "8w"]
box_dimensions = {2:[], 3:[], 5:[], 10:[], 20:[], 40:[]}
pop_size = {2:'100', 3:'120',5:'120',10:'140',20:'200',40:'250' }


for worker_index , file in enumerate(file_list):
    df = get_data_frame(file)
    for dim_index, (name, dim_group) in enumerate (df.groupby("dim")):
            #print(name)
            dim_instance = dim_group.groupby("instance").agg({'time_stamp':[np.min, np.max]})
            #print(dim_instance.ts.amax-dim_instance.ts.amin)
            time_diff_raw = dim_instance.time_stamp.amax-dim_instance.time_stamp.amin
            print(time_diff_raw)

            box_dimensions[name].append(list(map(lambda x: x.total_seconds(), time_diff_raw  )  ))




sns.set(style="darkgrid", palette="muted", color_codes=True)

f, axes = plt.subplots(1, 6)

for index , dim in enumerate([2, 3, 5, 10 ,20, 40]):
    ax = axes[index]
    ax.set_title(str(dim)+'D')
    #print(box_dimensions[dim])
    ax.boxplot(box_dimensions[dim], sym='',  labels=worker_labels)
    if index == 0:
        ax.set_ylabel("seconds" )

    ax.set_xlabel("pop size: {0}".format(pop_size[dim]) )
    #else:
    #    ax.set_ylabel("")

f.suptitle('5 sub-populations (messages)')
#plt.setp(axes)
plt.show()
