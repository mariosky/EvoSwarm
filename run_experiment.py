import redis
from datetime import datetime
import time
import sys
import json

import argparse

parser = argparse.ArgumentParser(description='Execute experiment in EvoSwarm')
parser.add_argument('--file', default='default_conf.json', help='Configuration file')
parser.add_argument('--host', default='localhost', help='Redis Host. Default is localhost')
parser.add_argument('--instances', default=15, help='How many instances of the experiment are needed')

args = parser.parse_args()
print(args.file)
print(args.host)





r = redis.Redis(host=args.host, port=6379, db=0)
id = int( datetime.timestamp(datetime.now()))


configuration = args.file

with open(configuration,"r") as conf:
    configuration_data = json.load(conf)

configuration_data['EXPERIMENT_ID'] = str(id)
configuration_data['INSTANCES'] = list(range(1,int(args.instances)+1))
    
print(configuration_data)

redis_ready = False 
while not redis_ready:
    try:
        redis_ready = r.ping()
    except:
        print("waiting for redis, press Ctrl+C to Quit")
        time.sleep(3)
    
print("redis alive")

r.rpush("setup_queue", json.dumps(configuration_data))

