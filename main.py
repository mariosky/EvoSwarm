from ga_worker import *
import redis
import json
import os
import time
import base64

# This function runs inside container together with a redis container

TOPIC_CONSUME =  ('TOPIC_CONSUME' in os.environ and os.environ['TOPIC_CONSUME']) or "population-objects"
TOPIC_PRODUCE =  ('TOPIC_CONSUME' in os.environ and os.environ['TOPIC_CONSUME']) or "evolved-population-objects"

r = redis.StrictRedis(host='localhost', port=6379, db=0)
producer = r.pubsub()
consumer = r.pubsub()
consumer.subscribe(TOPIC_CONSUME)




while True:
    message = consumer.get_message()
    if message:
        data_args = base64.b64decode(message['data'])
        args = json.loads(data_args)


        worker = GA_Worker(args)
        worker.setup()
        result = worker.run()

        # Return with a format for writing to MessageHub

        data = json.dumps(result).encode('utf-8')
        producer.publish(TOPIC_PRODUCE, data)


    else:
        time.sleep(.5)


