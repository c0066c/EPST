from __future__ import division
import random
import math
import numpy as np
import sys, getopt
from scipy.optimize import *
from sympy import *
from bounds import *
maxS = 10
delta = 0.1

def determineWorkload(task, higherPriorityTasks, criteria, time):
    workload = task[criteria]
    for i in higherPriorityTasks:
        jobs = math.ceil(time / i['period'])
        workload += jobs * i[criteria]
        #print("jobs " + repr(jobs) + " wl task " + repr(jobs * i[criteria]) + " total workload " + repr(workload))
    return workload

def findpoints(task, higherPriorityTasks, mode = 0):
    points = []
    if mode == 0: #kpoints
    # pick up k testing points here
        for i in higherPriorityTasks:
            point = math.floor(task['period']/i['period'])*i['period']
            if point != 0.0:
                points.append(point)
        points.append(task['period'])

    else: #allpoints
        for i in higherPriorityTasks:
            for r in range(1, int(math.floor(task['period']/i['period']))+1):
                point = r*i['period']
                if point != 0.0:
                    points.append(point)
        points.append(task['period'])

    return points

def ktda_allp(task, higherPriorityTasks, criteria, ieq, bound): #only for one deadline miss
    allpoints = []
    # pick up all testing points here
    allpoints = findpoints(task, higherPriorityTasks, 1)

    # for loop checking k points time
    minP = 1.
    for t in allpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        if ieq == Chernoff_bounds:
            try:
                # res = minimize_scalar(lambda x : ieq(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound])
                # probRes = ieq(task, higherPriorityTasks, fy, res.x)
                probRes = ieq(task, higherPriorityTasks, fy, 1)
            except TypeError:
                print "TypeError"
                probRes = 1
        elif ieq == Hoeffding_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        elif ieq == Bernstein_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        else:
            raise "Error: You use a bound without implementation."
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP


def ktda_p(task, higherPriorityTasks, criteria, ieq, bound): #only for one deadline miss
    kpoints = []
    # pick up k testing points here
    kpoints = findpoints(task, higherPriorityTasks, 0)

    # for loop checking k points time
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        if ieq == Chernoff_bounds:
            try:
                # res = minimize_scalar(lambda x : ieq(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound])
                # probRes = ieq(task, higherPriorityTasks, fy, res.x)
                tmplist = []
                for x in np.arange(0, maxS, delta):
                    tmplist.append(ieq(task, higherPriorityTasks, fy, x))
                probRes = min(tmplist)
            except TypeError:
                print "TypeError"
                probRes = 1
        elif ieq == Hoeffding_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        elif ieq == Bernstein_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        else:
            raise "Error: You use a bound without implementation."
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP

def ktda_k(task, higherPriorityTasks, criteria, window, ieq, bound):
    kpoints = []
    # pick up k testing points here
    if window != 1:
        for i in higherPriorityTasks:
            for j in range(1, window+1):
                point = math.floor((j)*task['period']/i['period'])*i['period']
                if point != 0.0:
                    kpoints.append(point)
        kpoints.append((window+1)*task['period'])
    else:
        kpoints = findpoints(task, higherPriorityTasks, 0)

    '''
    kpoints.sort()
    if len(higherPriorityTasks) == 9:
        print "dtda_points:\n"
        print kpoints
    '''
    # for loop checking k points time
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)

        if ieq == Chernoff_bounds:
            try:
                # res = minimize_scalar(lambda x : ieq(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound]) #find the x with minimum
                # probRes = ieq(task, higherPriorityTasks, fy, res.x) #use x to find the minimal
                tmplist = []
                for x in np.arange(0, maxS, delta):
                    tmplist.append(ieq(task, higherPriorityTasks, fy, x))
                probRes = min(tmplist)
            except TypeError:
                print "TypeError"
                probRes = 1
        elif ieq == Hoeffding_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        elif ieq == Bernstein_inequality:
            probRes = ieq(task, higherPriorityTasks, fy)
        else:
            raise "Error: You use a bound without implementation."

        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP


def kltda(task, higherPriorityTasks, criteria,  numDeadline, oneD, ieq, bound):
    #oneD is precalculated outside of function call
    if numDeadline == 0:
        return 1
    if numDeadline == 1:
        return oneD
    else:
        maxi = 0.
        for w in range(0, numDeadline):
            tmpP=ktda_k(task, higherPriorityTasks, criteria,  numDeadline-w, ieq, bound) * kltda(task, higherPriorityTasks, criteria, w,  oneD,  bound)
            if(tmpP > maxi):
                maxi = tmpP
        return maxi

def probabilisticTest_p(tasks, numDeadline, ieq, bound=1):
    seqP = []
    x = 0
    for i in tasks:
        hpTasks = tasks[:x]
        if numDeadline == 1:
            resP = ktda_p(i, hpTasks, 'abnormal_exe', ieq, bound)
        else:
            resP = kltda(i, hpTasks, 'abnormal_exe',  numDeadline, ktda_p(i, hpTasks, 'abnormal_exe', ieq, bound),bound)
        seqP.append(resP)
        x+=1
    return max(seqP)

def probabilisticTest_allp(tasks, numDeadline, ieq, bound=1):
    seqP = []
    x = 0
    for i in tasks:
        hpTasks = tasks[:x]
        if numDeadline == 1:
            resP = ktda_p(i, hpTasks, 'abnormal_exe', ieq, bound)
        else:
            resP = kltda(i, hpTasks, 'abnormal_exe',  numDeadline, ktda_p(i, hpTasks, 'abnormal_exe', ieq, bound),bound)
        seqP.append(resP)
        x+=1
    return max(seqP)

