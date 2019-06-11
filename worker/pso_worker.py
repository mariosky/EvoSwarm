import uuid
import os
import numpy as np

import pso


class PSO_Worker:
    def __init__(self, conf)
        self.conf = conf
        self.function = dictbbob[self.conf['problem']['function']](int(self.conf['problem']['instance']))
        self.F_opt = self.function.getfopt()
        self.deltaftarget = 1e-8
        self.worker_uuid = uuid.uuid1()

    def put_back(self, s):
        final_pop = [{"chromosome": tuple(ind), "id": None,
                      "fitness": {"DefaultContext": 0, "score": 0}} for ind in
                     s.pop]

        self.evospace_sample['sample'] = final_pop


        if 'benchmark' in self.conf:
            experiment_id = 'experiment_id' in conf and conf['experiment_id'] or 0
            self.evospace_sample['benchmark_data'] = {'params': self.params, 'evals': s.convergence, 'algorithm': 'PSO',
                                                      'benchmark': self.conf['function'],
                                                      'instance': self.conf['instance'],
                                                      'worker_id': str(self.worker_uuid),
                                                      'experiment_id': experiment_id,
                                                      'dim': self.conf['dim'],
                                                      'fopt': self.function.getfopt()
                                                      }
        self.space.put_sample(self.evospace_sample)

    def get_pop(self):
        pop = [cs['chromosome'] for cs in conf['population']]
        return np.array(pop)


    def run(self, pop):
        self.function.__name__ = "F%s instance %s" % (self.conf['function'], self.conf['instance'])
        self.params = {'NGEN': self.conf['NGEN'], 'sample_size': self.conf['sample_size'],
                       'init': 'random:[-5,5]'
                       }
        pop = self.get_pop()
        return pso.PSO(objf=self.function, dim=self.conf['problem']['dim'], iters=conf['algorithm']['iterations'], pos=pop, Vmax=conf['algorithm']['Vmax'], wMax=conf['algorithm']['wMax'], wMin=conf['algorithm']['wMin'],   fopt=self.function.getfopt())

def PSO(objf, dim, iters, pos, Vmax = 6, wMax = 0.9, wMin = 0.2, c1=2, c2 = 2, fopt=float("-inf") , **kwargs ):


 "algorithm": 