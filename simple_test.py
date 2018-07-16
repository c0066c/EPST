'''
Author: Kuan-Hsun Chen
'''
#import timing
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math
import random
import sys, getopt
import json
from scipy.optimize import *
from sympy import *

n = 3
PSet = []
Tpoints = []
overT = []
t=[]
maxS = 50
delta = 0.5

def selectedpoints(targetIdx):
#    math.ceil()
    tarT=PSet[targetIdx]

    for i in range(targetIdx):
        checkT = PSet[i]
        t = math.floor(tarT['period']/checkT['period'])*checkT['period']
        Tpoints.append(t)

    Tpoints.append(tarT['period'])

def taskInit():
    #task 1
    pair = {}
    pair['period'] = 10
#    pair['NWCET'] = 6
#    pair['AWCET'] = 8
    pair['NWCET'] = 4
    pair['AWCET'] = 6
    pair['prob'] = 0.000001
    PSet.append(pair)
    #task 2
    pair = {}
    pair['period'] = 45
    pair['NWCET'] = 10
    pair['AWCET'] = 15
#    pair['NWCET'] = 2
#    pair['AWCET'] = 3
    pair['prob'] = 0.000001
    PSet.append(pair)
    #task 3

    pair = {}
    pair['period'] = 75
    pair['NWCET'] = 10
    pair['AWCET'] = 30
    pair['prob'] = 0.000001
    PSet.append(pair)


def Chernoff_bounds(a, t):
    #timing.log("Chernoff bound starts")
    '''
    return the probability, input the targeted time point a and t
    1. first calculate the total number of jobs among all tasks
    2. calculate mgf function for each task with their corresponding number jobs in nlist
    3. using input t \in {0, b} to find the minimal result
    '''
    #input a is the selected point
    prob = np.float128(1.0)
    prob = prob/exp(t*a)
    count = 0
    #now sumN is the total number of jobs among all the tasks.
    c1, c2, x, p = symbols("c1, c2, x, p")
    expr = exp(c1*x)*(1-p)+exp(c2*x)*p
    mgf = lambdify((c1, c2, x, p), expr)
    nlist=[]
    for i in range(n):
        nlist.append(np.ceil(a/PSet[i]['period']))
    for i in nlist:
        prob = prob * np.float128(mgf(PSet[count]['NWCET'], PSet[count]['AWCET'], t, PSet[count]['prob']))**int(i)
        count += 1
    #timing.log("Chernoff bound ends")
    return prob

taskInit()
#timing.log("Task init")
selectedpoints(n-1)#3 tasks use 2, 2 tasks use 1
#timing.log("Select k points")
pResult = .0
minP=1.
plt.title('Probability of P(S>=a)')
plt.xlabel('t')
plt.ylabel('Probability')

for y in Tpoints:
    fy=float(y)
    tmplist = []
    for x in np.arange(0, maxS, delta):
        tmplist.append(Chernoff_bounds(fy, x))
    probRes=min(tmplist)
    print "On time point "+str(fy)+" the minimal probability is "+str(probRes)
    if minP > probRes:
        minP = probRes
print "Among all the selected points, the minimal upper bound is:"+str(minP)


#plt.axis([0.1, 0.3, 0, 1])
#plt.axis([0.5, 2, 0, 0.05])
#plt.plot(t, overT,'ro')
#plt.plot(t, overT)
#plt.show()
