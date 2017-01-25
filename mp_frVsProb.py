from multiprocessing import Pool, freeze_support
import itertools
import random
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import matplotlib.pyplot as plt
import itertools
import EPST
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
name='test'

# Information about the general task set
tasksinBkt = [5, 10]

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6.]
hardTaskFactor = [wcetF2]
numDeadline = [1]

tasks=[]
def func_star(a_b):
    """Covert 'f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call."""
    return insideroutine(*a_b)

def insideroutine(numberOfRuns, fr):
    c_prob = []
    seq_prob = []
    for i in range(numberOfRuns):
        tasks=[]
        tasks=task_generator.taskGeneration_p(20,60)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
        print tasks
        #the following part is for testing
        #c_prob.append(cprta.cprta(tasks))
        seq_prob.append(EPST.probabilisticTest_p(tasks, 3, 3))
    return [c_prob,seq_prob]

for tib in tasksinBkt:
    perfault = []
    cfault = []
    for fr in faultRate:
        numberOfRuns = 5
        print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(1)+', FaultRate:'+repr(10**-6.)+', Utilization:'+repr(60))
        rel=[]
        faultrel=[]
        crel=[]
        if __name__=='__main__':
            freeze_support()
            p = Pool(5)
            a_arg = [1,1,1,1,1]
            rel = (p.map(func_star, itertools.izip(a_arg, itertools.repeat(fr))))

        print rel
        for i in rel:
            crel.append(i[0])
            faultrel.append(i[1])
        cfault.append(crel)
        perfault.append(faultrel)

fileName = 'mp_CR_EPST_utilization'+repr(60)
folder = 'comparison/'
file = open(folder + 'txt/' +  fileName + '.txt', "w")
file.write('Runs: ' + repr(500) + '\n')
file.write('Tasks: ' + repr(tib) + '\n')
file.write('Num of deadline miss: ' + repr(1) + '\n')
file.write('Utilization: '+repr(60) + '\n')
numberOfRuns = 5
for j in tasksinBkt:
    for i in range(numberOfRuns):
        file.write('Generated '+ repr(j) +'Tasks:'+repr(i)+'\n')
        tasks=[]
        tasks=task_generator.taskGeneration_p(j,60)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
        for k in tasks:
            file.write(repr(k) + ',')
            file.write('\n')

        file.write('\n')

file.write('DMP:\n')
for i,m in zip(perfault, cfault):
    file.write('kp:\n')
    for j in i:
        file.write(repr(j) + ',')
    file.write('\n')
    file.write('\n')
    file.write('convolution:\n')
    for j in m:
        file.write(repr(j) + ',')

file.close()

