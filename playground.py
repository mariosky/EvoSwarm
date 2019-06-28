
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from itertools import groupby
from operator import itemgetter


messages = []
grp_benchmark = itemgetter("benchmark","dim")
grp_instance = itemgetter("benchmark","instance")
result = []

new_info = True
data = None
#with open(r'experiment_data\1561177738\swarm_ea_1561177738.json') as json_file:  
#with open(r'experiment_data\1561185389\swarm_ea_1561185389.json') as json_file:      
#    data = json.load(json_file)
#    for d in data:
#        print( d["benchmark"] , d["dim"], d["instance"])

#print(data[0])


#for dim_key, benchmark_group in groupby(data, grp_benchmark):
#    print(dim_key, benchmark_group)
with open(r'D:\exp_data\1561526317_1w\swarm_ea_1561526317.json') as json_file: 
#with open(r'experiment_data\1561185389\swarm_ea_1561185389.json') as json_file:  
    data = json.load(json_file)
    #print(data[0])
    for p in data:
       dt_object = datetime.fromtimestamp(p['time_stamp'])
       #print(p["dim"], p["instance"])
       messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))

labels = ['ts','n','dim','instance','best_score','fopt']
sns.set(style="white", palette="muted", color_codes=True)

f, axes = plt.subplots(1, 6, sharex=True, sharey=True)

#sns.despine(left=True)





df = pd.DataFrame.from_records(messages, columns=labels)
#df.set_index('ts', drop=False, inplace=True)
#group_by_dim = df.groupby("dim")

#for name, group in group_by_dim:
#        #print(group.n.resample('120S').sum())
#        print(group.agg( {'ts':[np.min, np.max]} ))
        
#print(group_by_dim.agg( {'ts':[np.min, np.max]} ))
#df2 = group_by_dim.resample('60S').agg( {'ts':[np.min, np.max] , 'n':np.sum })



resample_step = {2:'20S', 3:'20S',5:'20S',10:'60S',20:'120S',40:'240S' }

#for name, group in df2:
#        print (df2.get_group(group))
#        print (name, group)
        #sns.barplot(x=group.ts, y=group.n.sum, palette="rocket")
for i, (name, group) in enumerate (df.groupby("dim")):
        group.set_index('ts', drop=False, inplace=True)
        print(name)
        resample = group.resample(resample_step[name]).agg( {'ts':[np.min, np.max] , 'n':np.sum })
        sns.barplot(x=resample.ts.amax, y=resample.n['sum'], color="b", ax=axes[i])
#for i, (name, group) in enumerate (df2.reset_index().groupby('dim')):
        #sns.barplot(x=list(group.ts.amax), y=list(group.n.sum), palette="rocket")
        #print([i for i in group.n['sum']] , list( range(1, len(group.n['sum']) + 1 )))
        print(resample)
        #for i in group.ts.amax:
        #        print (i)
        #sns.barplot(x=group.ts.amax, y=group.n['sum'], palette="rocket", ax=axes[count])

plt.setp(axes, xticks=[])
#plt.tight_layout()
plt.show()
#print(df2.ts.amin)

#df2.reset_index().plot(kind='bar', use_index=True, y='n')

# from rx import Observable, Observer
# from rx.subjects import Subject

# messages = Subject()

# valid_messages = messages.take(8)\
#                    .filter(lambda s: s[0] == 1 ) \
#                    .publish()

# valid_messages.subscribe(lambda s : print(s))

# valid_messages.buffer_with_count(2)\
#               .subscribe(lambda s : print( s))

# valid_messages.connect()
# for s in  [ (1, "ABB", 1)  ,(1, "BCC", 2),(1, "DBA", 3),
#             (1, "AAA", 4)  ,(1, "AAA", 5),(1, "AAA", 6),
#             (1, "AAA", 7)  ,(1, "AAA", 8),(1, "AAA", 9),
#             (3, "AAA", 10) ,(31, "AAA", 11) ]  :

#     messages.on_next(s)
