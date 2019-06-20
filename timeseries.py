


import json
import pandas as pd

from datetime import datetime

messages = []

with open('D:\\exp_data\\1561049018\\swarm_ea_1561049018.json') as json_file:  
    data = json.load(json_file)
    for p in data:
        dt_object = datetime.fromtimestamp(p['time_stamp'])
        messages.append((pd.to_datetime(dt_object) , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

print(messages[:3])
labels = ['ts','dim','instance','best_score','fopt']

df = pd.DataFrame.from_records(messages, columns=labels)
