import redis

import sys
import json

r = redis.Redis(host='localhost', port=6379, db=0)

if len(sys.argv) > 1 :
    configuration =  sys.argv[1]
else:
    configuration = "default_conf.json"

with open(configuration,"r") as conf:
    configuration_data = json.load(conf)

print(configuration_data)
r.rpush("setup_queue", json.dumps(configuration_data))
