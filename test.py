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