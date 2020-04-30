


import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime




# 1, 2, 4, 8 workers
file_list = [r'C:\F4Exp\swarm_ea_1w_5m.json',
             r'C:\F4Exp\swarm_ea_2w_5m.json',
             r'C:\F4Exp\swarm_ea_4w_5m.json',
             r'C:\F4Exp\swarm_ea_8w_5m.json']

def get_data_frame(file):
    messages = []
    with open(file) as json_file: 
        data = json.load(json_file)
        for p in data:
            dt_object = datetime.fromtimestamp(p['time_stamp'])
            messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))
    return pd.DataFrame.from_records(messages, columns=labels)



labels = ['ts','n','dim','instance','best_score','fopt']
sns.set(style="darkgrid", palette="muted", color_codes=True)

f, axes = plt.subplots(4, 6, sharex=True, sharey='col')

#sns.despine(left=True)
resample_step = {2:'2S', 3:'5S',5:'10S',10:'30S',20:'60S',40:'100S' }
worker_labels = ["1w", "2w", "4w", "8w"]
for worker_index , file in enumerate(file_list):
    df = get_data_frame(file)
    for dim_index, (name, group) in enumerate (df.groupby("dim")):
            group.set_index('ts', drop=False, inplace=True)
            resample = group.resample(resample_step[name]).agg( {'ts':[np.min, np.max] , 'n':np.sum })
            ax = axes[worker_index, dim_index]
            print(worker_labels[worker_index] ,name, resample )
            print(len(resample))
            sns.lineplot(x=list(range(len(resample))), y=resample.n['sum'], color="b", ax=ax)
            if dim_index == 0:
                ax.set_ylabel(worker_labels[worker_index] )
            else:
                ax.set_ylabel("")
            
            if worker_index == len(worker_labels)-1:
                 ax.set_xlabel("{0} second sample".format(resample_step[name][:-1]) )
            else:
                ax.set_xlabel("")
            
            if worker_index == 0:
                ax.set_title('{}D'.format(name))

f.suptitle('Number of Populations (Messages)')
plt.setp(axes)
plt.show()
