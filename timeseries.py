


import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime



messages = []

# These files are in each folder 

w1 = 'swarm_ea_1561054780.json'
w2 = 'swarm_ea_1561074987.json'
w4 = 'swarm_ea_1561082965.json'
w8 = 'swarm_ea_1561087340.json'
with open(w1) as json_file:  
    data = json.load(json_file)
    for p in data:
        dt_object = datetime.fromtimestamp(p['time_stamp'])
        messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

labels = ['ts','n','dim','instance','best_score','fopt']

df = pd.DataFrame.from_records(messages, columns=labels)
df.set_index('ts', drop=False, inplace=True)

df.n.resample('10S').sum().plot()

with open(w2) as json_file:  
    data = json.load(json_file)
    for p in data:
        dt_object = datetime.fromtimestamp(p['time_stamp'])
        messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

df = pd.DataFrame.from_records(messages, columns=labels)
df.set_index('ts', drop=False, inplace=True)

df.n.resample('10S').sum().plot()

with open(w4) as json_file:  
    data = json.load(json_file)
    for p in data:
        dt_object = datetime.fromtimestamp(p['time_stamp'])
        messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

df = pd.DataFrame.from_records(messages, columns=labels)
df.set_index('ts', drop=False, inplace=True)

df.n.resample('10S').sum().plot()

with open(w8) as json_file:  
    data = json.load(json_file)
    for p in data:
        dt_object = datetime.fromtimestamp(p['time_stamp'])
        messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

df = pd.DataFrame.from_records(messages, columns=labels)
df.set_index('ts', drop=False, inplace=True)

df.n.resample('10S').sum().plot()

plt.show()