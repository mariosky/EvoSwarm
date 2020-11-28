from ga_worker import *
from pso_worker import *
import redis
import json
import os
import time
import base64
import uuid



TOPIC_CONSUME =   "population-objects"
TOPIC_PRODUCE =   "evolved-population-objects"
WORKER_ID = str (uuid.uuid4())

r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=6379, db=0)
redis_ready = False 
while not redis_ready:
    try:
        redis_ready = r.ping()
    except:
        print("waiting for redis")
        time.sleep(3)
    
print("redis alive")


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
        args["worker_id"] =  WORKER_ID

        if args["algorithm"] == "GA":
            worker = GA_Worker(args)
            worker.setup()
            result = worker.run()
        else:
            worker = PSO_Worker(args)

            result = worker.run()
            #print("result:",result)

       
       # Return with a format for writing to MessageHub
        #print(result['population'])
        data = json.dumps(result).encode('utf-8')
        print("New POPULATION Message")
        #r.publish(TOPIC_PRODUCE, data)
        r.rpush(TOPIC_PRODUCE, data)

    else:
        #print("no message")
        time.sleep(1)


