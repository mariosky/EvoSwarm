import redis
import os
import logging
import time
import datetime
import json
import uuid

logger = logging.getLogger('google_experiment')
logger.setLevel(logging.INFO)

TOPIC_PRODUCE =  ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "population-objects"
MESSAGE_TYPE = ('MESSAGE_TYPE' in os.environ and os.environ['MESSAGE_TYPE']) or 'QUEUE'

print(os.environ['MESSAGE_TYPE'])

r = redis.StrictRedis(host='redis', port=6379, db=0)

conf = {
#Example from EvoSpace
# Parameter configuration for each dimension 10**5 * D
# 2: 200,000
# 3: 300,000
# 5: 500,000

# 40: 4,000,000

    2: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':20, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':6 },
    3: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':30, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
    5: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
    10:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':8 },
    20:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':8 },
    40:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':16 },



    'EXPERIMENT_ID' : int(time.time()),

     #For paper:
    'FUNCTIONS' : (3,),
    'DIMENSIONS' : (10, ),       #(2,3,5,10,20)
    'INSTANCES' : (1, )  #list(range(1,6)) + list(range(41, 51))

}

def new_populations(env, number_of_pops, n_individuals, dim, lb, ub ):
    import random
    message_list = []
    for pop in range(number_of_pops):
        new_env = dict(env)
        new_env["population"] = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n_individuals)]
        new_env["message_id"] = str (uuid.uuid4())
        message_list.append(new_env)
    return message_list



def experiment(conf):
    for function in  conf['FUNCTIONS']:
        for dim in conf['DIMENSIONS'] :
            logger.info ("DIM:{} ".format( dim))
            for instance in conf['INSTANCES'] :
                logger.info ("instance:{}".format(instance))

                env = {"problem":
                            {"name": "BBOB",
                              "instance": instance,
                              "error": 1e-8,
                              "function": function,
                              "dim": dim,
                              "search_space": [-5, 5],
                              "problem_id": "%s-%s-%s-%s" % ( conf['EXPERIMENT_ID'] , function, instance, dim ),
                              "max_iterations": conf[dim]['MAX_ITERATIONS'] * conf[dim]['MESSAGES_HUB_GA'] },
                 "population": [],
                 "population_size": conf[dim]['POP_SIZE'],
                 "id": "1",
                 "algorithm": {"crossover": {"type": "cxTwoPoint", "CXPB_RND": [0.2, 0.6], "CXPB": 0.2}, "name": "GA",
                               "mutation": {"MUTPB": 0.5, "indpb": 0.05, "sigma": 0.5, "type": "mutGaussian", "mu": 0},
                               "selection": {"type": "tools.selTournament", "tournsize": 2},
                               "iterations": conf[dim]['NGEN']},
                 "experiment":
                     {"owner": "mariosky", "type": "benchmark", "experiment_id": conf['EXPERIMENT_ID']}}

                #Initialize pops
                google_messages = new_populations(env, conf[dim]['MESSAGES_HUB_GA'] , conf[dim]['POP_SIZE'],env["problem"]["dim"], env["problem"]["search_space"][0], env["problem"]["search_space"][1])
                print("messages created")

                print("Checking redis with ping")
                while not r.ping():
                    print("ping",r.ping())
                    time.sleep(1)

                
                for data in google_messages:
                    json_data = json.dumps(data)
                    # Data must be a bytestring
                    message = json_data.encode('utf-8')
                    print("message")
                    if MESSAGE_TYPE == 'QUEUE':
                        print("sending to",TOPIC_PRODUCE )
                        result = r.lpush(TOPIC_PRODUCE, message)
                        print("lpush", result)
                
                print(function,dim, instance )
                print ("First Messages Sent")
                print ("Begin Message Loop")



if __name__ == '__main__':
    DESTINATION_PATH = r'/Users/mariogarcia-valdez/Desktop/CocoExp/'
    PROJECT_PATH = r'/Users/mariogarcia-valdez/evocloud/'

    experiment(conf)
