import uuid
import os
import numpy as np
from bbobbenchmarks import *
import pso


class PSO_Worker:
    def __init__(self, conf):
        self.conf = conf
        self.function = dictbbob[self.conf['problem']['function']](int(self.conf['problem']['instance']))
        self.F_opt = self.function.getfopt()
        self.deltaftarget = 1e-8
        self.worker_uuid = uuid.uuid1()

    # def put_back(self, s):
       

    #     self.evospace_sample['sample'] = final_pop


    #     if 'benchmark' in self.conf:
    #         experiment_id = 'experiment_id' in conf and conf['experiment_id'] or 0
    #         self.evospace_sample['benchmark_data'] = {'params': self.params, 'evals': s.convergence, 'algorithm': 'PSO',
    #                                                   'benchmark': self.conf['function'],
    #                                                   'instance': self.conf['instance'],
    #                                                   'worker_id': str(self.worker_uuid),
    #                                                   'experiment_id': experiment_id,
    #                                                   'dim': self.conf['dim'],
    #                                                   'fopt': self.function.getfopt()
    #                                                   }
    #     self.space.put_sample(self.evospace_sample)

    def get_pop(self):
        pop = [cs['chromosome'] for cs in self.conf['population']]
        return np.array(pop)


    def run(self):
        pop = self.get_pop()
        solution =  pso.PSO(objf=self.function, dim=self.conf['problem']['dim'],
            iters=self.conf['params']['PSO']['iterations'], pos=pop, Vmax=self.conf['params']['PSO']['Vmax'],
            wMax=self.conf['params']['PSO']['wMax'], wMin=self.conf['params']['PSO']['wMin'],   fopt=self.function.getfopt())
        final_pop = [{"chromosome": tuple(ind), "id": None,
                      "fitness": {"DefaultContext": 0, "score": 0}} for ind in
                     solution.pop]

        self.conf.update({'iterations': solution.convergence, 'population': final_pop, 'best_individual': solution.best ,
                          'fopt': self.function.getfopt(), 'best_score':solution.bestScore})

        if (solution.bestScore <= self.function.getfopt() + 1e-8):
            self.conf['best'] = True
        else:
            self.conf['best'] = False
        
        return self.conf
