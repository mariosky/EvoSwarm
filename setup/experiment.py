import redis
import os
#import process_logs
import logging
import time
#import pytz
import datetime
import json

logger = logging.getLogger('google_experiment')
logger.setLevel(logging.INFO)

TOPIC_NAME =  ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "population-objects"
MESSAGE_TYPE = ('MESSAGE_TYPE' in os.environ and os.environ['MESSAGE_TYPE']) or 'PUBSUB'

print(os.environ['MESSAGE_TYPE'])

r = redis.StrictRedis(host='redis', port=6379, db=0)

conf = {
#Example from EvoSpace
# Parameter configuration for each dimension 10**5 * D
# 2: 200,000
# 3: 300,000
# 5: 500,000

# 40: 4,000,000

    2: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':20, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
    3: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':30, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':2 },
    5: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
    10:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':4 },
    20:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':8 },
    40:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_HUB_PSO':0, 'MESSAGES_HUB_GA':16 },



    'EXPERIMENT_ID' : int(time.time()),

     #For paper:
    'FUNCTIONS' : (3,),
    'DIMENSIONS' : (2, ),       #(2,3,5,10,20)
    'INSTANCES' : (1, )  #list(range(1,6)) + list(range(41, 51))

}

# fh = logging.FileHandler('experiment_data/{}.log'.format( conf['EXPERIMENT_ID']))
# fh.setLevel(logging.INFO)
# logger.addHandler(fh)




def new_populations(env, number_of_pops, n_individuals, dim, lb, ub ):
    import random
    message_list = []
    for pop in range(number_of_pops):
        new_env = dict(env)
        new_env["population"] = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n_individuals)]

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
                print(google_messages)

                
                for data in google_messages:
                    json_data = json.dumps(data)
                    # Data must be a bytestring
                    message = json_data.encode('utf-8')

                    if MESSAGE_TYPE == 'QUEUE':
                        r.lpush(TOPIC_NAME, message)



                #Initialize experiment?






                #google_producer.send_messages(google_messages)
                #kafka_producer.send_messages(kafka_messages,'populations-topic')
                
                
                print(function,dim, instance )
                print ("First Messages Sent")
                print ("Begin Message Loop")

                #time.sleep(60)

                #google_controller.experiment(env)

                #Block until this experiment is done, redis queue, time_out
                #task = r.blpop("experiment_finished", 0)


                #print (task, "Done")







if __name__ == '__main__':
    DESTINATION_PATH = r'/Users/mariogarcia-valdez/Desktop/CocoExp/'
    PROJECT_PATH = r'/Users/mariogarcia-valdez/evocloud/'
    #start_time = datetime.datetime.fromtimestamp(time.time(), pytz.utc)
    #tz = pytz.timezone('UTC')
    #logger.info("Start: {}".format(tz.normalize(start_time.astimezone(tz)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
    experiment(conf)

    #finish_time = datetime.datetime.fromtimestamp(time.time(), pytz.utc)
    #logger.info("Start: {}".format(tz.normalize(finish_time.astimezone(tz)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')))

    #data_folder = process_logs.process_logs(conf['EXPERIMENT_ID'])
    #print ("python -m cocopp -o "+ DESTINATION_PATH + str(conf['EXPERIMENT_ID'])+ " " + PROJECT_PATH + data_folder[2:])