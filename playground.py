
import json
import pandas as pd
import matplotlib.pyplot as plt
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
with open(r'experiment_data\1561178365\swarm_ea_1561178365.json') as json_file:      
    data = json.load(json_file)
    for d in data:
        print( d["benchmark"] , d["dim"], d["instance"])

#print(data[0])


for dim_key, benchmark_group in groupby(data, grp_benchmark):
    print(dim_key, benchmark_group)

#with open('swarm.json') as json_file:  
#    data = json.load(json_file)
#    for p in data:
        #dt_object = datetime.fromtimestamp(p['time_stamp'])
        #print(p["dim"], p["instance"])
        #messages.append((pd.to_datetime(dt_object), 1 , p["dim"], p["instance"],  p["best_score"],  p["fopt"]))


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
