from rx import Observable
from rx.subjects import Subject
import redis
import os
import json
import random
import sys
import time

TOPIC_CONSUME =  ('TOPIC_CONSUME' in os.environ and os.environ['TOPIC_CONSUME']) or "evolved-population-objects"
TOPIC_PRODUCE =  ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "population-objects"
MESSAGE_TYPE = ('MESSAGE_TYPE' in os.environ and os.environ['MESSAGE_TYPE']) or 'QUEUE'

r = redis.StrictRedis(host='redis', port=6379, db=0)
consumer = r.pubsub()
consumer.subscribe(TOPIC_CONSUME)


def cxBestFromEach(pop1, pop2, key = lambda p: p['fitness']['score']):
    # small is better
    pop1.sort(key=key)
    pop2.sort(key=key)
    size = min(len(pop1), len(pop2))

    cxpoint = (size - 1) // 2

    pop1[cxpoint:] = pop2[:cxpoint+2]
    return pop1


class DockerExperiment():
    def __init__(self, env):
        self.state = "work"
        self.env = env
        self.consumed_messages = Subject()
        self.messages = Subject()
        self.population_objects_topic = "population-objects"
        self.consumed_messages\
            .take(env["problem"]["max_iterations"])\
            .buffer_with_count(3)\
            .subscribe( on_next=lambda x : self.population_mixer(x),on_completed = self.finish)

        self.consumed_messages.subscribe(lambda x : print('CONSUMED:{}'.format('x')),on_completed = lambda :"MESSAGES COMPLETED"  )
        self.messages.publish()

        self.messages.subscribe(lambda populations : self.produce(populations), on_completed = lambda :"MESSAGES COMPLETED" )

        self.read_from_queue()

    def finish(self):

        print("Consume Finished")
        self.status = "stop"
        self.messages.on_completed()
        self.messages.dispose()
        sys.exit(0)



        

    def population_mixer(self, populations):
        if len(populations) == 3:
            print("MIXER:",len(populations))
            #populations = [json.loads(message.data) for message in populations]
            populations[0]['population'] = cxBestFromEach(populations[0]['population'],populations[1]['population'])
            populations[1]['population'] = cxBestFromEach(populations[1]['population'], populations[2]['population'])
            populations[2]['population'] = cxBestFromEach(populations[2]['population'], populations[0]['population'])

            # I can´t fo map(...on_next, populations )
            self.messages.on_next(populations[0])
            self.messages.on_next(populations[1])
            self.messages.on_next(populations[2])
            
        
    
    def read_from_queue(self):
        print("worker start")
        while self.state == 'work':
            data = None
            if MESSAGE_TYPE ==  'PUBSUB':
                message = consumer.get_message()
                if message and message['type'] == 'message':
                    data = message['data']
    
            elif MESSAGE_TYPE ==  'QUEUE':
                message =  r.blpop(TOPIC_CONSUME, 2)
                if message:
                    data = message[1]
                    
                else:
                    print("NO DATA, WAITING...")
                    #break
            if data:
                pop_dict = json.loads(data)
                log_to_redis_coco(pop_dict)
                #print("message:data:", pop_dict)
                #print("message:type:", type(pop_dict))
                if 'best_score' in pop_dict:

                    print (pop_dict['best_score'] )
                print("message read from queue")
                self.consumed_messages.on_next(pop_dict)
            else:
                print("no message")
                time.sleep(1)

    def produce(self, population):
        print("pop sent:", "population")
        json_data = json.dumps(population)
        # Data must be a bytestring
        message = json_data.encode('utf-8')


        if MESSAGE_TYPE == 'QUEUE':
            ack = r.lpush(TOPIC_PRODUCE, message)
            print("Produce:", ack)

def log_to_redis_coco(population):
    #log_name = 'log:test_pop:' + str(population['experiment']["experiment_id"])
    log_name =  "log:swarm"
    r.lpush(log_name, json.dumps(get_benchmark_data(population)))




def get_benchmark_data(population):
    return {"evals": population["iterations"],
            "instance":population["problem"]["instance"],
            "worker_id":"NA",
            "params":{"sample_size":population["population_size"],
                      "init":"random:[-5,5]",
                      "NGEN":population["algorithm"]["iterations"]
                      },
             "experiment_id":population['experiment']["experiment_id"],
             "algorithm":population["algorithm"]["name"],
             "dim":population["problem"]["dim"],
             "benchmark":population["problem"]["function"],
             "fopt":population["fopt"]}


DockerExperiment({"problem":{"max_iterations":100}})
time.sleep(4)

