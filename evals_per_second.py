import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from itertools import groupby
from operator import itemgetter



# 1, 2, 4, 8 workers
file_list = [r'C:\F4Exp\swarm_ea_1w_5m.json',
             r'C:\F4Exp\swarm_ea_2w_5m.json',
             r'C:\F4Exp\swarm_ea_4w_5m.json',
             r'C:\F4Exp\swarm_ea_8w_5m.json']

labels = ['ts','n','dim','instance','evals']

def get_data_frame(file):
    messages = []
    with open(file) as json_file: 
        data = json.load(json_file)
        
        for p in data:
            evals =  sum([e['num_of_evals'] for e in   p['evals']])
            dt_object = datetime.fromtimestamp(p['time_stamp'])
            messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"], evals))
    return pd.DataFrame.from_records(messages, columns=labels)

get_data_frame(file_list[0])