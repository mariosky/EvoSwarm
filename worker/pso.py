# -*- coding: utf-8 -*-
"""
From 
Vmahttps://github.com/mariosky/EvoloPy

Forked from

https://github.com/7ossam81/EvoloPy
Created on Sun May 15 22:37:00 2016
@author: Hossam Faris
"""

import random
import numpy
import math
import time

class solution:
    def __init__(self):
        self.best = 0
        self.bestIndividual=[]
        self.convergence = []
        self.optimizer=""
        self.objfname=""
        self.startTime=0
        self.endTime=0
        self.executionTime=0
        self.lb=0
        self.ub=0
        self.dim=0
        self.popnum=0
        self.maxiers=0




def PSO(objf, dim, iters, pos, Vmax = 6, wMax = 0.9, wMin = 0.2, c1=2, c2 = 2, fopt=float("-inf") , **kwargs ):


    s=solution()
    PopSize = len(pos)
    
    
    ######################## Initializations
    
    vel=numpy.zeros((PopSize,dim))
    
    pBestScore=numpy.zeros(PopSize) 
    pBestScore.fill(float("inf"))
    
    pBest=numpy.zeros((PopSize,dim))
    gBest=numpy.zeros(dim)
    
    
    gBestScore=float("inf")
   
    convergence_curve=[]
    
    
    timerStart=time.time() 
    s.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    
    for l in range(0,iters):
        for i in range(0,PopSize):
            pos[i,:]=numpy.clip(pos[i,:], -5, 5)
            #Calculate objective function for each particle
            fitness=objf(pos[i,:])
    
            if(pBestScore[i]>fitness):
                pBestScore[i]=fitness
                pBest[i,:]=pos[i,:]
                
            if(gBestScore>fitness):
                gBestScore=fitness
                gBest=pos[i,:]
        
        #Update the W of PSO
        w=wMax-l*((wMax-wMin)/iters);
        
        for i in range(0,PopSize):
            for j in range (0,dim):
                r1=random.random()
                r2=random.random()
                vel[i,j]=w*vel[i,j]+c1*r1*(pBest[i,j]-pos[i,j])+c2*r2*(gBest[j]-pos[i,j])
                
                if(vel[i,j]>Vmax):
                    vel[i,j]=Vmax
                
                if(vel[i,j]<-Vmax):
                    vel[i,j]=-Vmax
                            
                pos[i,j]=pos[i,j]+vel[i,j]
        
        #convergence_curve[l]=gBestScore
        convergence_curve.append({"gen_num":l,"best_fitness":gBestScore,"best_solution":list(gBest), "num_of_evals":PopSize })

        
      

    timerEnd=time.time()
    s.bestScore=gBestScore
    s.best = list(gBest)
    s.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    s.executionTime=timerEnd-timerStart
    s.convergence=list(convergence_curve)
    s.pop = list(pos)

    return s