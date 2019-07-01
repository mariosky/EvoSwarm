
import urllib.parse, ast
import os, redis, json
import sys
from coco import CoCoData
from itertools import groupby
from operator import itemgetter
 

def process_logs(experiment_id, list_name = "log:swarm", redis_host = 'localhost', redis_port = 6379):
    r = redis.Redis(host=redis_host, port=redis_port)

    DATA_FOLDER = './experiment_data/' + str(experiment_id) + '/'
    experiment = 'swarm_ea' +'_' + str(experiment_id)
    data = [json.loads(i) for i in r.lrange( list_name, 0, -1) if json.loads(i)['experiment_id'] == str(experiment_id)]
    #data = [json.loads(i) for i in r.lrange(experiment, 0, -1)]
    #data.reverse()

    #IF not exisits
    try:
        os.makedirs(DATA_FOLDER)
    except OSError:
        pass
    with open(DATA_FOLDER+experiment+'.json', 'w') as f:
        for d in data:
            f.write( json.dumps(d) +'\n')
           #json.dump(data, f)


    grp_benchmark = itemgetter("benchmark","dim")
    grp_instance = itemgetter("benchmark","instance")
    result = []
    new_info = True
    for dim_key, benchmark_group in groupby(data, grp_benchmark):
        #Create folder if not exisits
        folder = DATA_FOLDER + '/F' + str(dim_key[0])
        try:
            os.makedirs(folder)
        except OSError:
            pass

        indexfile = DATA_FOLDER + '%s.info' % ( '/F' + str(dim_key[0]))

        # Create files
        filename = '%s-%02d_f%s_DIM%d' % (str(experiment_id), 0,
                                          str(dim_key[0]), dim_key[1])
        datafile =  folder+'/' + filename + '.tdat'
        hdatafile = folder+'/' + filename + '.dat'

        print ("F" + str(dim_key[0]) + " Dimension:" + str(dim_key[1]))

        comment = "% SwarmEA: Message Based Algorithm see info in root folder"
        if new_info:
            info = """funcId = %s, DIM = %d, Precision = 1.000e-08, algId = 'SwarmEA'\n%s\nF%s/%s.dat, """ % \
               (str(dim_key[0]), dim_key[1], comment, dim_key[0],filename)
            new_info = False
        else:
            info = """\nfuncId = %s, DIM = %d, Precision = 1.000e-08, algId = 'SwarmEA'\n%s\nF%s/%s.dat, """ % \
                   (str(dim_key[0]), dim_key[1], comment, dim_key[0], filename)


        f = open(indexfile, 'a')
        f.writelines(info)

        f.close()
        new_instance = True

        for instance_key,benchmark in groupby(benchmark_group, grp_instance):
            print  (" Instance:" + str(instance_key[1]))


            coco = CoCoData(dim_key[1], function= dim_key[0], instance= instance_key[1] )
            index = 0
            total = 0
            buffr = []
            hbuffr =[]

            for row in benchmark:
                data_row = []
                row_id=0
                for e in row['evals']:
                    # We have to change this to a more practical solution

                    num_evals = row['params']['sample_size']
                    
                    if len(e) >= 4:
                        num_evals = e['num_of_evals']


                    data_row.append((e['best_fitness'], row['algorithm'], e['gen_num'],num_evals, e['best_fitness'],row['fopt'], '%+10.9e'% ( e['best_fitness']-row['fopt']),e[ 'best_solution']))
                    row_id+=1
                data_row.sort(reverse=True)
                for r in data_row:
                    coco.evalfun(*r[1:],buffr=buffr,hbuffr=hbuffr)

            if buffr:
                f = open(datafile, 'a')
                f.write('%% function evaluation | noise-free fitness - Fopt'
                        ' (%13.12e) | best noise-free fitness - Fopt | measured '
                        'fitness | best measured fitness | x1 | x2...\n' % row['fopt']
                        )


                f.writelines(buffr)

                f.close()
            if hbuffr:
                f = open(hdatafile, 'a')
                f.write('%% function evaluation | noise-free fitness - Fopt'
                        ' (%13.12e) | best noise-free fitness - Fopt | measured '
                        'fitness | best measured fitness | x1 | x2...\n' % row['fopt']
                        )
                f.writelines(hbuffr)
                f.close()


            last = buffr[-1].split(" ")






            f = open(indexfile, 'a')
            if new_instance:
                f.write('%s:%d|%.1e' % (instance_key[1],int(last[0]), float(last[1])))
                new_instance = False
            else:
                f.write(', %s:%d|%.1e' % (instance_key[1], int(last[0]), float(last[1])))

            f.close()
    return DATA_FOLDER

if __name__ == "__main__":
    process_logs(sys.argv[1])
