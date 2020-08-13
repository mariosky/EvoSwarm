import json
import pandas as pd

# First we must state if the jsonfile has lines
LINES = True

in_file = r'C:\Users\mario\Desktop\experiments\16w05mEC2.json'
out_file = None




if not out_file:
    out_file = in_file[:-4]+'csv'

if LINES:
    with open(in_file) as json_file: 
        chunk = pd.read_json(json_file,lines =True, chunksize = 5000)
        for data in chunk:
            data.drop(['alg_params', 'evals', 'algorithm', 'best_score', 'experiment_id',
                       'message_counter', 'message_id', 'params', 'worker_id', 'benchmark'], axis=1)

            data['num_evals'] = [sum(map(lambda r: r['num_of_evals'], row)) for row in data.evals]
            data.to_csv(out_file, index=False, header=False, mode='a', columns = [ 'dim', 'instance', 'time_stamp', 'num_evals'] )

else:
    data = pd.read_json(in_file)

    #data.drop(['alg_params','evals', 'algorithm', 'best_score', 'experiment_id',
    #        'message_counter', 'message_id', 'params', 'worker_id','benchmark'], axis = 1 )#\

    data['num_evals'] = [sum(map(lambda r: r['num_of_evals'], row)) for row in data.evals]
    data.to_csv(out_file, index=False, header=False, mode='a', columns = [ 'dim', 'instance', 'time_stamp', 'num_evals'] )
