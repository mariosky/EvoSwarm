# swarm-ga-worker

Stateless Genetic Algorithm Worker


```
 "algorithm": {"crossover": {"type": "cxTwoPoint", "CXPB_RND": conf["CXPB_RND"] },
                               "name": "GA",
                               "mutation": {"MUTPB_RND":conf["MUTPB_RND"], "indpb": 0.05, "sigma": 0.5, "type": "mutGaussian", "mu": 0},
                               "selection": {"type": "tools.selTournament", "tournsize": 2},
                               "iterations": conf["DIM_CONFIGURATION"][str(dim)]['NGEN']},
```

## Run

Redis needs to be stopped before this, because it uses the same port.

You will need to use 

    pip install -r requirements.txt
    
to install the needed library files.

After `docker-compose up`, which starts the services

## COCO

### Run
```
python coco_process_logs.py <EXPERIMENT_ID>
```

### COCO Post-processing
More details in (https://github.com/numbbo/coco)
```
git clone https://github.com/numbbo/coco.git

python do.py install-postprocessing

python -m cocopp [-o OUTPUT_FOLDERNAME] YOURDATAFOLDER [MORE_DATAFOLDERS]
```

