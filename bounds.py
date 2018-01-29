from __future__ import division
import random
import math
import numpy as np
import sys, getopt
from scipy.optimize import *
from sympy import *

# Assume the input tasks only have two modes: c1 and c2.

def Chernoff_bounds(task, higherPriorityTasks, t, s):
    #t is the tested time t, s is a real number, n is the total number of involved tasks
    '''
    return the upper bounded probability, input the targeted time point t and a real number s
    1. first calculate the total number of jobs among all tasks
    2. calculate mgf function for each task with their corresponding number jobs in nlist
    3. using input t \in {0, b} to find the minimal result
    '''
    prob = 1.0
    #now sumN is the total number of jobs among all the tasks.
    c1, c2, x, p = symbols("c1, c2, x, p")
    expr = exp(c1*x)*(1-p)+exp(c2*x)*p
    mgf = lambdify((c1, c2, x, p), expr)
    #with time ceil(), what's the # of released jobs
    for i in higherPriorityTasks:
        prob = prob * (mgf(i['execution'], i['abnormal_exe'], s, i['prob']))**int(math.ceil(t/i['period']))
    #itself
    prob = prob * (mgf(task['execution'], task['abnormal_exe'], s, task['prob']))**int(math.ceil(t/task['period']))
    prob = prob/exp(s*t)

    return prob

def Hoeffding_inequality(task, higherPriorityTasks, t):
    #t is the tested time t, s is a real number, n is the total number of involved tasks
    '''
    return the upper bounded probability, input the targeted time point t.
    '''
    prob = 1.0
    expdSt = 0.0
    sumvar = 0.0
    c1, c2, p = symbols("c1, c2, p")
    sumr = lambdify((c1, c2, p), c1*(1-p)+c2*p)
    # here c1 is ai and c2 is bi
    vari = lambdify((c1, c2), (c2-c1)**2)

    for i in higherPriorityTasks:
        expedSt = expedSt + sumr(i['execution'], i['abnormal_exe'], i['prob'])*int(math.ceil(t/i['period']))
        sumvar = sumvar + vari(i['execution'], i['abnormal_exe'])*int(math.ceil(t/i['period']))
    expedSt = expedSt + sumr(task['execution'], task['abnormal_exe'], task['prob'])*int(math.ceil(t/task['period']))
    sumvar = sumvar + vari(task['execution'], task['abnormal_exe'])*int(math.ceil(t/task['period']))

    prob = exp(-2*(t-expedSt)**2/sumvar)
    return prob


def Bernstein_inequality(task, higherPriorityTasks, t):
    #t is the tested time t, s is a real number, n is the total number of involved tasks
    prob = 1.0

    return prob
