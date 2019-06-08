from elasticsearch import Elasticsearch
client = Elasticsearch()

response = client.search(
    index="swarm",
    body={
        "query": { 
            "bool":{ 
            "filter":[ 
            {"term": { "experiment_id" : 1559616805}}
        ] 
    }
  },
  "size":100,
  "sort" : [{"message_counter" : {"order" : "asc"}} ] ,
  "_source": ["best_score","message_counter" ]
  
}
)

for hit in response['hits']['hits']:
    print(hit)

from rx import Observable
Observable.range(0, 100).filter(lambda x : x > 3).take(20).buffer_with_count(2).subscribe(on_next=lambda x : print(x), on_completed = lambda : print("D"))

import redis
import json

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
    "EXPERIMENT_ID" : "1234",

    "FUNCTIONS": [3,4],
    "DIMENSIONS" : [10],
    "INSTANCES" : [1,2,3],  
    "CXPB_RND": [0.2, 0.6],
    "MUTPB_RND": [0.1, 0.3]
}
""" 
r.rpush("experiment_queue" ,y)