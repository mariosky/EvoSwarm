
import random
from bbobbenchmarks import *

import uuid


from deap import base
from deap import creator
from deap import tools

class GA_Worker:
    def __init__(self, conf):
        self.conf = conf
        self.function = dictbbob[self.conf['problem']['function']](int(self.conf['problem']['instance']))
        self.F_opt = self.function.getfopt()
        self.function_evaluations = 0 #Is not needed in EvoWorkers, they dont know the number of FE
        self.deltaftarget = 1e-8
        self.toolbox = base.Toolbox()
        self.FC = 0
        self.worker_uuid = uuid.uuid1()
        self.space = None
        self.evospace_sample = {'sample':conf['population']}

    def setup(self):
        if "FitnessMin" not in dir(creator):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))     #Minimizing Negative
        if "Individual" not in dir(creator):
            creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, -5, 5)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_float, self.conf['problem']['dim'])
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.eval)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=self.conf['params']['GA']['mutation']['mu'], sigma=self.conf['params']['GA']['mutation']['sigma'], indpb=self.conf['params']['GA']['mutation']['indpb'])
        self.toolbox.register("select", tools.selTournament, tournsize=self.conf['params']['GA']['selection']['tournsize'])

    def eval(self, individual):
        return  self.function(individual),

    def get(self):
        pop = []

        for cs in self.evospace_sample['sample']:
            ind = creator.Individual(cs['chromosome'])
            if 'score' in cs['fitness']:
                ind.fitness = creator.FitnessMin(values=(cs['fitness']['score'],))
            pop.append(ind)

        return pop


    def run(self):
        evals = []
        num_fe_first_sample = 0
        first_sample = True


        #random.seed(i)

        CXPB = self.conf['params']['GA']['crossover']['CXPB']
        MUTPB = self.conf['params']['GA']['mutation']['MUTPB']
        
        NGEN = self.conf['params']['GA']['iterations']
        pop = self.get()


        # Evaluate the entire population
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        num_fe_first_sample += len(invalid_ind)

        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit


        # Begin the evolution
        for g in range(NGEN):
            num_fe = 0
            #print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            #print("  Evaluated %i individuals" % len(invalid_ind))
            num_fe = num_fe + len(invalid_ind)

            # The population is entirely replaced by the offspring
            pop[:] = offspring
            #print(pop)

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            evals.append({"gen_num":g,"best_fitness":min(fits),"best_solution":tools.selBest(pop, 1)[0], "num_of_evals":num_fe })


        best_ind = tools.selBest(pop, 1)[0]

        final_pop = [{"chromosome": ind[:], "id": None,
                     "fitness": {"DefaultContext": ind.fitness.values[0], "score": ind.fitness.values[0]}}
                     for ind in pop]

        self.conf.update({'iterations': evals, 'population': final_pop, 'best_individual': best_ind ,
                          'fopt': self.function.getfopt(), 'best_score':best_ind.fitness.values[0]})

        if (best_ind.fitness.values[0] <= self.function.getfopt() + 1e-8):
            self.conf['best'] = True
        else:
            self.conf['best'] = False
        
        #print("Worker", self.conf)

        return self.conf