
import urllib.parse, ast
import os, redis, json
import sys
from coco import CoCoData
from itertools import groupby
from operator import itemgetter
 

def process_logs(list_name = "log:swarm", redis_host = 'localhost', redis_port = 6379):
    r = redis.Redis(host=redis_host, port=redis_port)

    DATA_FOLDER = './experiment_data/'
    
    data = [json.loads(i) for i in r.lrange( list_name, 0, -1)]
    #data.reverse()

    #IF not exisits
    try:
        os.makedirs(DATA_FOLDER)
    except OSError:
        pass

    with open(DATA_FOLDER+'redis_log.json', 'w') as f:
        json.dump(data, f)

    return DATA_FOLDER

if __name__ == "__main__":
    folder = process_logs()
    print(folder)    