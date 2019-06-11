# swarm-ga-worker
Stateless Genetic Algorithm Worker


´´´
 "algorithm": {"crossover": {"type": "cxTwoPoint", "CXPB_RND": conf["CXPB_RND"] },
                               "name": "GA",
                               "mutation": {"MUTPB_RND":conf["MUTPB_RND"], "indpb": 0.05, "sigma": 0.5, "type": "mutGaussian", "mu": 0},
                               "selection": {"type": "tools.selTournament", "tournsize": 2},
                               "iterations": conf["DIM_CONFIGURATION"][str(dim)]['NGEN']},
´´´´