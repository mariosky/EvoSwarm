from ga_worker import *
import redis
import json
import os
import time
import base64

# This function runs inside container together with a redis container

TOPIC_CONSUME =  ('TOPIC_CONSUME' in os.environ and os.environ['TOPIC_CONSUME']) or "population-objects"
TOPIC_PRODUCE =  ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "evolved-population-objects"
MESSAGE_TYPE = ('MESSAGE_TYPE' in os.environ and os.environ['MESSAGE_TYPE']) or 'PUBSUB'

r = redis.StrictRedis(host='redis', port=6379, db=0)
print(os.environ['MESSAGE_TYPE'])
consumer = r.pubsub()
consumer.subscribe(TOPIC_CONSUME)

# {'type': 'subscribe', 'pattern': None, 'channel': b'population-objects', 'data': 1}
while True:
    data = None
    if MESSAGE_TYPE ==  'PUBSUB':
        message = consumer.get_message()
        if message and message['type'] == 'message':
            data = message['data']
    
    elif MESSAGE_TYPE ==  'QUEUE':
        message =  r.blpop(TOPIC_CONSUME)
        data = message[1]
    
    
    
    if data:
        #print(data)
        
        #data_args = base64.b64decode(data)
        args = json.loads(data)
        worker = GA_Worker(args)
        worker.setup()
        result = worker.run()
       # Return with a format for writing to MessageHub
        data = json.dumps(result).encode('utf-8')

        r.publish(TOPIC_PRODUCE, data)
        r.lpush(TOPIC_CONSUME, data)

    else:
        #print("no message")
        time.sleep(1)


