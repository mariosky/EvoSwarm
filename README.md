# EvoSwarm

Stateless Multi-populatonm Algorithm in Docker containers.

## Requeriments

1. You need docker,  docker-compose
2. A git client
3. Python3


## Install

1. Clone this repo
```
git clone https://github.com/mariosky/EvoSwarm.git
```
2. From the root of the project:

    You will need to use 
```
    pip3 install -r requirements.txt
```    
   to install the needed library files.


## Run the service

Your local Redis needs to be stopped before this, because it uses the same port.
After `docker-compose up`, which downloads and starts the services. 
Wait until the controller is ready:
```
controller_1  | waiting for experiment
controller_1  | pulling   
```

## Execute an experiment

From another terminal add or modify a json configuration file
and add a new experiment to the queue:
```
python3 run_experiment.py your_conf.json 
```

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

