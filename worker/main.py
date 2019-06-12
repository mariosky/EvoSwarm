from ga_worker import *
from pso_worker import *
import redis
import json
import os
import time
import base64

# This function runs inside container together with a redis container

TOPIC_CONSUME =   "population-objects"
TOPIC_PRODUCE =   "evolved-population-objects"


r = redis.StrictRedis(host='redis', port=6379, db=0)



# {'type': 'subscribe', 'pattern': None, 'channel': b'population-objects', 'data': 1}
while True:
    data = None
    print("worker LOOP")

    message =  r.blpop(TOPIC_CONSUME)
    # message is a tuple (queue_name, data)
    data = message[1] 
    print("message:from::", TOPIC_CONSUME)
        #print("message:type:", type(data))
    
    if data:
        #print(data)
        
        #data_args = base64.b64decode(data)
        args = json.loads(data)

       
        result = None
        print(args["algorithm"])

        if args["algorithm"] == "GA":
            worker = GA_Worker(args)
            worker.setup()
            result = worker.run()
        else:
            worker = PSO_Worker(args)

            result = worker.run()
            #print("result:",result)

       
       # Return with a format for writing to MessageHub
        data = json.dumps(result).encode('utf-8')
        print("New POPULATION Message")
        r.publish(TOPIC_PRODUCE, data)
        r.lpush(TOPIC_PRODUCE, data)

    else:
        #print("no message")
        time.sleep(1)


