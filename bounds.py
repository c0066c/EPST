from __future__ import division
import random
import math
import numpy as np
import sys, getopt
from scipy.optimize import *
from sympy import *


def Chernoff_bounds(task, higherPriorityTasks, a, t):
    #a is the selected points, t is the testing t, n is the total number of involved tasks
    '''
    return the probability, input the targeted time point a and t
    1. first calculate the total number of jobs among all tasks
    2. calculate mgf function for each task with their corresponding number jobs in nlist
    3. using input t \in {0, b} to find the minimal result
    '''
    #input a is the selected point
    prob = 1.0
    #now sumN is the total number of jobs among all the tasks.
    c1, c2, x, p = symbols("c1, c2, x, p")
    expr = exp(c1*x)*(1-p)+exp(c2*x)*p
    mgf = lambdify((c1, c2, x, p), expr)
    #with time ceil(), what's the # of released jobs
    for i in higherPriorityTasks:
        prob = prob * (mgf(i['execution'], i['abnormal_exe'], t, i['prob']))**int(math.ceil(a/i['period']))
    #itself
    prob = prob * (mgf(task['execution'], task['abnormal_exe'], t, task['prob']))**int(math.ceil(a/task['period']))
    prob = prob/exp(t*a)

    return prob

def Hoeffding_inequality(task, higherPriorityTasks, a, t):
    #a is the selected points, t is the testing t, n is the total number of involved tasks
    '''
    return the probability, input the targeted time point a and t
    1. first calculate the total number of jobs among all tasks
    2. calculate mgf function for each task with their corresponding number jobs in nlist
    3. using input t \in {0, b} to find the minimal result
    '''

    return prob

def Bernstein_inequality(task, higherPriorityTasks, a, t):
    #a is the selected points, t is the testing t, n is the total number of involved tasks
    return prob

