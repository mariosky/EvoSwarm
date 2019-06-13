import redis
from datetime import datetime

import sys
import json

r = redis.Redis(host='localhost', port=6379, db=0)
id = int( datetime.timestamp(datetime.now()))

if len(sys.argv) > 1 :
    configuration =  sys.argv[1]
else:
    configuration = "default_conf.json"

with open(configuration,"r") as conf:
    configuration_data = json.load(conf)

configuration_data['EXPERIMENT_ID'] = str(id)
configuration_data['INSTANCES'] = []
for i in range(15):
    configuration_data['INSTANCES'].append(i+1)
    
print(configuration_data)

r.rpush("setup_queue", json.dumps(configuration_data))

