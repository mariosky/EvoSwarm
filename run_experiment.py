import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

y = """
{
"DIM_CONFIGURATION" : 
    {
        "2" : { "NGEN":50, "POP_SIZE": 100, "MAX_ITERATIONS":20, "MESSAGES_PSO":0, "MESSAGES_GA":6 },
        "3" : { "NGEN":50, "POP_SIZE": 100, "MAX_ITERATIONS":30, "MESSAGES_PSO":0, "MESSAGES_GA":2 },
        "5": { "NGEN":50, "POP_SIZE": 100, "MAX_ITERATIONS":25, "MESSAGES_PSO":0, "MESSAGES_GA":4 },
        "10":{ "NGEN":50, "POP_SIZE": 100, "MAX_ITERATIONS":25, "MESSAGES_PSO":0, "MESSAGES_GA":8 },
        "20":{ "NGEN":50, "POP_SIZE": 200, "MAX_ITERATIONS":25, "MESSAGES_PSO":0, "MESSAGES_GA":8 },
        "40":{ "NGEN":50, "POP_SIZE": 200, "MAX_ITERATIONS":25, "MESSAGES_PSO":0, "MESSAGES_GA":16 }
    },
    "EXPERIMENT_ID" : "314152",
    "GA_WORKER_RATIO" : 0.5,

    "FUNCTIONS": [4],
    "DIMENSIONS" : [10],
    "INSTANCES" : [1,2,3],  
    "CXPB_RND": [0.2, 0.6],
    "MUTPB_RND": [0.1, 0.3]
}
"""

r.rpush("setup_queue", y)
