


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
             r'D:\exp_data\1561521129_4w\swarm_ea_1561521129.json',
             r'D:\exp_data\1561516494_8w\swarm_ea_1561516494.json']

def get_data_frame(file):
    messages = []
    with open(file) as json_file: 
        data = json.load(json_file)
        for p in data:
            dt_object = datetime.fromtimestamp(p['time_stamp'])
            messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))
    return pd.DataFrame.from_records(messages, columns=labels)



labels = ['ts','n','dim','instance','best_score','fopt']


#sns.despine(left=True)
resample_step = {2:'2S', 3:'5S',5:'10S',10:'30S',20:'60S',40:'100S' }
worker_labels = ["1w", "2w", "4w", "8w"]
box_dimensions = {2:[], 3:[], 5:[], 10:[], 20:[], 40:[]}

for worker_index , file in enumerate(file_list):
    df = get_data_frame(file)
    for dim_index, (name, dim_group) in enumerate (df.groupby("dim")):
            #print(name)
            dim_instance = dim_group.groupby("instance").agg({'ts':[np.min, np.max]})
            #print(dim_instance.ts.amax-dim_instance.ts.amin)
            time_diff_raw = dim_instance.ts.amax-dim_instance.ts.amin

            box_dimensions[name].append(list(map(lambda x: x.total_seconds(), time_diff_raw  )  ))


            #group.set_index('ts', drop=False, inplace=True)
            #resample = group.resample(resample_step[name]).agg( {'ts':[np.min, np.max] , 'n':np.sum })
            #ax = axes[worker_index, dim_index]
            #print(worker_labels[worker_index] ,name, resample )
            #print(len(resample))
            #sns.lineplot(x=list(range(len(resample))), y=resample.n['sum'], color="b", ax=ax)
            #if dim_index == 0:
            #    ax.set_ylabel(worker_labels[worker_index] )
            #else:
            #    ax.set_ylabel("")
            
            #if worker_index == len(worker_labels)-1:
            #     ax.set_xlabel("{0} second sample".format(resample_step[name][:-1]) )
            #else:
            #    ax.set_xlabel("")
            
            #if worker_index == 0:
            #    ax.set_title('{}D'.format(name))




sns.set(style="darkgrid", palette="muted", color_codes=True)

f, axes = plt.subplots(1, 6)

for index , dim in enumerate([2, 3, 5, 10 ,20, 40]):
    ax = axes[index]
    ax.set_title(str(dim)+'D')
    #print(box_dimensions[dim])
    ax.boxplot(box_dimensions[dim], sym='',  labels=worker_labels)

    if index == 0:
        ax.set_ylabel("seconds" )
    #else:
    #    ax.set_ylabel("")


#plt.setp(axes)
plt.show()