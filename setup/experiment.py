import redis
import os
import logging
import time
import datetime
import json
import uuid

#logger = logging.getLogger('google_experiment')
#logger.setLevel(logging.INFO)

TOPIC_PRODUCE =  ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "population-objects"
WORKER_HEARTBEAT_INTERVAL = 10


r = redis.StrictRedis(host='redis', port=6379, db=0)

conf = {
#Example from EvoSpace
# Parameter configuration for each dimension 10**5 * D
# 2: 200,000
# 3: 300,000
# 5: 500,000

# 40: 4,000,000
"DIM_CONFIGURATION" : {
    2: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':20, 'MESSAGES_PSO':0, 'MESSAGES_GA':6 },
    3: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':30, 'MESSAGES_PSO':0, 'MESSAGES_GA':2 },
    5: { 'NGEN':50, 'POP_SIZE': 100, 'MAX_ITERATIONS':25, 'MESSAGES_PSO':0, 'MESSAGES_GA':4 },
    10:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_PSO':0, 'MESSAGES_GA':8 },
    20:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_PSO':0, 'MESSAGES_GA':8 },
    40:{ 'NGEN':50, 'POP_SIZE': 200, 'MAX_ITERATIONS':25, 'MESSAGES_PSO':0, 'MESSAGES_GA':16 }
    },



    'EXPERIMENT_ID' : int(time.time()),

    'FUNCTIONS' : [3],
    'DIMENSIONS' : [10],       #(2,3,5,10,20)
    'INSTANCES' : [1],  #list(range(1,6)) + list(range(41, 51))
    "CXPB_RND": [0.2, 0.6],
    "MUTPB_RND": [0.1, 0.3],
}

def new_populations(env, number_of_pops, n_individuals, dim, lb, ub ):
    import random
    message_list = []
    for pop in range(number_of_pops):
        new_env = dict(env)
        new_env["population"] = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n_individuals)]
        new_env["message_id"] = str (uuid.uuid4())
        
        new_env['algorithm']['crossover']['CXPB']  = random.uniform(conf['CXPB_RND'][0],conf['CXPB_RND'][1])
        new_env['algorithm']['mutation']['MUTPB']  = random.uniform(conf['MUTPB_RND'][0],conf['MUTPB_RND'][1])
        
        
        message_list.append(new_env)
    return message_list



def experiment(conf):
    print("conf", conf)
    for function in  conf['FUNCTIONS']:
        for dim in conf['DIMENSIONS'] :
            for instance in conf['INSTANCES']:
                env = {"problem":
                            {"name": "BBOB",
                              "instance": instance,
                              "error": 1e-8,
                              "function": function,
                              "dim": dim,
                              "search_space": [-5, 5],
                              "problem_id": "%s-%s-%s-%s" % ( conf['EXPERIMENT_ID'] , function, instance, dim ),
                              "max_iterations": conf["DIM_CONFIGURATION"][str(dim)]['MAX_ITERATIONS'] * conf["DIM_CONFIGURATION"][str(dim)]['MESSAGES_GA'] },
                 "population": [],
                 "population_size": conf["DIM_CONFIGURATION"][str(dim)]['POP_SIZE'],
                 "id": "1",
                 "algorithm": {"crossover": {"type": "cxTwoPoint", "CXPB_RND": conf["CXPB_RND"] },
                               "name": "GA",
                               "mutation": {"MUTPB_RND":conf["MUTPB_RND"], "indpb": 0.05, "sigma": 0.5, "type": "mutGaussian", "mu": 0},
                               "selection": {"type": "tools.selTournament", "tournsize": 2},
                               "iterations": conf["DIM_CONFIGURATION"][str(dim)]['NGEN']},
                 "experiment":
                     {"type": "benchmark", "experiment_id": conf['EXPERIMENT_ID']}}

                #Initialize pops
                _messages = new_populations(env, conf["DIM_CONFIGURATION"][str(dim)]['MESSAGES_GA'] , conf["DIM_CONFIGURATION"][str(dim)]['POP_SIZE'],env["problem"]["dim"], env["problem"]["search_space"][0], env["problem"]["search_space"][1])
                print("messages created")

                print("Checking redis with ping")
                while not r.ping():
                    print("ping",r.ping())
                    time.sleep(1)

                
                for data in _messages:
                    json_data = json.dumps(data)
                    # Data must be a bytestring
                    message = json_data.encode('utf-8')
                    print("message")
                    
                    print("sending to",TOPIC_PRODUCE )
                    result = r.lpush(TOPIC_PRODUCE, message)
                    print("lpush", result)

                
                print(function,dim, instance )
                print ("First Messages Sent")
                
                print("Sending message to controller")
                
                r.rpush("experiment_queue",json.dumps(env))
                #Block Until Finsihed
                experiment_finished = r.blpop("experiment_finished", 0)
                print (experiment_finished, "Done")

                #Return
                print ("Begin Message Loop")



def pull_conf(time_out=WORKER_HEARTBEAT_INTERVAL):
        #Pop task from queue
        #This is a blocking operation
        #task is a tuple (queue_name, task_id)
        task = r.blpop("experiment_queue", time_out)
        if task:
            print("Task:", task)
            #Get Task Details
            #_task = r.get(task[1])
            #Get Time_stamp
            #time_stamp =r.time()[0]
            #Store task in pending_set ordered by time
            # zadd NOTE: The order of arguments differs from that of the official ZADD command.
            #r.zadd(self.cola.pending_set,  '%s:%s' % (self.id, task[1]), time_stamp)
            # Return a Task object
            #return Task(**eval(_task))
        #If there is no task to do return None
            
            return task
        else:
            return ()


if __name__ == '__main__':
    while True:
        config_message = pull_conf()
        print(config_message)

        if (config_message):
            config_json = config_message[1]
            config = json.loads(config_json)
            experiment(config)
        else:
            pass
