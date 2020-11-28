import redis
import os
import logging
import time
import datetime
import json
import uuid

TOPIC_PRODUCE = ('TOPIC_PRODUCE' in os.environ and os.environ['TOPIC_PRODUCE']) or "population-objects"
WORKER_HEARTBEAT_INTERVAL = 10

r = redis.StrictRedis(host='localhost', port=6379, db=0)

redis_ready = False
while not redis_ready:
    try:
        redis_ready = r.ping()
    except:
        print("waiting for redis")
        time.sleep(3)

print("setup:redis alive")


config = {
    "DIM_CONFIGURATION" :
    {
        "10":{ "NGEN":50, "POP_SIZE": 100, "MAX_ITERATIONS":25, "MESSAGES_PSO":0, "MESSAGES_GA":8 }
    },
    "GA_WORKER_RATIO" : 0.5,
    "FUNCTIONS": [4],
    "DIMENSIONS" : [10],
    "CXPB_RND": [0.2, 0.6],
    "MUTPB_RND": [0.1, 0.3],
    "INSTANCES": [1,2],
    "EXPERIMENT_ID":1
}


def new_populations(env, conf, number_of_pops, n_individuals, dim, lb, ub):
    import random
    message_list = []
    for _ in range(number_of_pops):
        new_env = dict(env)
        new_env["population"] = [
            {"chromosome": [random.uniform(lb, ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}}
            for _ in range(n_individuals)]
        new_env["message_id"] = str(uuid.uuid4())
        if random.random() > env["experiment"]["ga_worker_ratio"]:
            new_env["algorithm"] = "PSO"
        else:
            new_env["algorithm"] = "GA"
        new_env['params']['GA']['crossover']['CXPB'] = random.uniform(conf['CXPB_RND'][0], conf['CXPB_RND'][1])
        new_env['params']['GA']['mutation']['MUTPB'] = random.uniform(conf['MUTPB_RND'][0], conf['MUTPB_RND'][1])
        message_list.append(new_env)
    return message_list


def experiment(conf):
    print("conf", conf)
    for function in conf['FUNCTIONS']:
        for dim in conf['DIMENSIONS']:
            for instance in conf['INSTANCES']:
                env = {"problem":
                           {"name": "BBOB",
                            "instance": instance,
                            "error": 1e-8,
                            "function": function,
                            "dim": dim,
                            "search_space": [-5, 5],
                            "problem_id": "%s-%s-%s-%s" % (conf['EXPERIMENT_ID'], function, instance, dim),
                            "max_iterations": conf["DIM_CONFIGURATION"][str(dim)]['MAX_ITERATIONS'] *
                                              conf["DIM_CONFIGURATION"][str(dim)]['MESSAGES_GA']},
                       "population": [],
                       "population_size": conf["DIM_CONFIGURATION"][str(dim)]['POP_SIZE'],
                       "id": "1",
                       "algorithm": None,
                       "params": {"GA":
                                      {"crossover": {"type": "cxTwoPoint", "CXPB_RND": conf["CXPB_RND"]},
                                       "mutation": {"MUTPB_RND": conf["MUTPB_RND"], "indpb": 0.05, "sigma": 0.5,
                                                    "type": "mutGaussian", "mu": 0},
                                       "selection": {"type": "tools.selTournament", "tournsize": 2},
                                       "iterations": conf["DIM_CONFIGURATION"][str(dim)]['NGEN'],

                                       },
                                  "PSO":
                                  # Acording to https://sci2s.ugr.es/sites/default/files/files/TematicWebSites/EAMHCO/contributionsGECCO09/p2269-elabd.pdf
                                      {"Vmax": 5,
                                       "wMax": 0.9,
                                       "wMin": 0.2,
                                       "c1": 2,
                                       "c2": 2,
                                       "iterations": conf["DIM_CONFIGURATION"][str(dim)]['NGEN']
                                       }
                                  },

                       "experiment":
                           {"type": "benchmark", "experiment_id": conf['EXPERIMENT_ID'],
                            "ga_worker_ratio": conf['GA_WORKER_RATIO']}}

                # Initialize pops
                _messages = new_populations(env, conf, conf["DIM_CONFIGURATION"][str(dim)]['MESSAGES_GA'],
                                            conf["DIM_CONFIGURATION"][str(dim)]['POP_SIZE'], env["problem"]["dim"],
                                            env["problem"]["search_space"][0], env["problem"]["search_space"][1])
                print("messages created")

                print("Checking redis with ping")
                while not r.ping():
                    print("ping", r.ping())
                    time.sleep(1)

                for data in _messages:
                    json_data = json.dumps(data)
                    # Data must be a bytestring
                    message = json_data.encode('utf-8')
                    print("message")

                    print("sending to", TOPIC_PRODUCE)
                    result = r.rpush(TOPIC_PRODUCE, message)
                    print("rpush", result)

                print(function, dim, instance)
                print("populations sent to workers")

                print("sending problem to controller")

                r.rpush("experiment_queue", json.dumps(env))
                # Block Until Finsihed
                print("waiting for problem to finish")

                experiment_finished = r.blpop("experiment_finished", 0)
                print(experiment_finished, "Done")

                # Return
                print("Begin Message Loop")

experiment(config)
