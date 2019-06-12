import numpy as np
import worker.bbobbenchmarks as bn
import random

class CoCoData(object):
    def __init__(self, dim, function, instance, nbptsevals= 20, nbptsf = 5):
        self.evalsTrigger = 1
        self.function = function
        self.instance = instance
        self.lasteval_num = 0
        self.fTrigger = np.inf
        self.idxFTrigger = np.inf
        self.nbptsf = nbptsf
        self.idxEvalsTrigger = 0
        self.nbptsevals = nbptsevals
        self.dim = dim
        self.idxDIMEvalsTrigger = 0.
        self.nbFirstEvalsToAlwaysWrite = 1


    def evalfun(self, algorithm, gen, ngen, fmin, fopt, error, sol,buffr=None,hbuffr=None):
        fmin = float(fmin)
        fopt = float(fopt)

        error = float(error)

        self.lasteval_num = self.lasteval_num + int(ngen)

        if (self.lasteval_num >= self.evalsTrigger or fmin  - fopt < self.fTrigger):
            #We must write if we are past the trigger?

            if self.lasteval_num >= self.evalsTrigger:
                #In order to pass an assertion in DataSet() we add a fake first eval using a random solution
                if not buffr:
                    #buffr.append(self.sprintData(1, algorithm, gen, ngen, fmin, fopt, error, sol))
                    random_sol =  [10. * random.random() - 5 for _ in range(self.dim)]
                    function = bn.dictbbob[self.function](self.instance)
                    fval = function(random_sol)
                    fopt = function.getfopt()
                    buffr.append(self.sprintData(1, algorithm, gen, ngen, fval, fopt, fopt - fval, random_sol))

                buffr.append(self.sprintData(self.lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol))

                while self.lasteval_num >= np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)):
                    self.idxEvalsTrigger += 1
                while self.lasteval_num >= self.dim * 10 ** self.idxDIMEvalsTrigger:
                    self.idxDIMEvalsTrigger += 1
                self.evalsTrigger = min(np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)),
                                        self.dim * 10 ** self.idxDIMEvalsTrigger)
                if self.lasteval_num < self.nbFirstEvalsToAlwaysWrite:
                    self.evalsTrigger = self.lasteval_num + 1

            # Also if we have a better solution
            if fmin - fopt < self.fTrigger:  # minimization only
                if not hbuffr:
                    random_sol = [10. * random.random() - 5 for _ in range(self.dim)]
                    function = bn.dictbbob[self.function](self.instance)
                    fval = function(random_sol)
                    fopt = function.getfopt()
                    hbuffr.append(self.sprintData(1, algorithm, gen, ngen, fval, fopt, fopt - fval, random_sol))

                    #hbuffr.append(self.sprintData(1, algorithm, gen, ngen, fmin, fopt, error, sol))
                hbuffr.append(self.sprintData(self.lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol))
                if fmin <= fopt:
                    self.fTrigger = -np.inf
                else:
                    if np.isinf(self.idxFTrigger):
                        self.idxFTrigger = np.ceil(np.log10(fmin - fopt)) * self.nbptsf
                    while fmin - fopt <= 10 ** (self.idxFTrigger / self.nbptsf):
                        self.idxFTrigger -= 1
                    self.fTrigger = min(self.fTrigger, 10 ** (self.idxFTrigger / self.nbptsf))  # TODO: why?



    def sprintData(self, lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol):
        """Format data for printing."""

        res = ('%d %+10.9e %+10.9e %+10.9e %+10.9e'
               % (lasteval_num, fmin - fopt,
                  fmin - fopt, fmin,
                  fopt))

        if len(sol) < 22:
            tmp = []
            for i in sol:
                tmp.append(' %+5.4e' % i)
            res += ''.join(tmp)
        res += '\n'
        return res