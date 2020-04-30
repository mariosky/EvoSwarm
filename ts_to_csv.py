import json
import pandas as pd

# First we must state if the jsonfile has lines
LINES = True

in_file = r'D:\exp_data\1562080407_1w_10m\swarm_ea_1562080407.json'
out_file = None

if not out_file:
    out_file = in_file[:-4]+'csv'

if LINES:
    with open(in_file) as json_file: 
    #with open(r'experiment_data\1561185389\swarm_ea_1561185389.json') as json_file:  
        chunk = pd.read_json(json_file,lines =True, chunksize = 5000  )
        for data in chunk:
            
            data.drop(['alg_params','evals', 'algorithm', 'best_score', 'experiment_id', 
                'message_counter', 'message_id', 'params', 'worker_id','benchmark'], axis = 1 )\
                .to_csv(out_file, index=False, header=False, mode='a', columns = [ 'dim', 'instance', 'time_stamp'] )

else:
    data = pd.read_json(in_file)
    data.drop(['alg_params','evals', 'algorithm', 'best_score', 'experiment_id', 
            'message_counter', 'message_id', 'params', 'worker_id','benchmark'], axis = 1 )\
        .to_csv(out_file, index=False, header=False, mode='a', columns = [ 'dim', 'instance', 'time_stamp'] )