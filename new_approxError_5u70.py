import cprta
import random
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import EPST
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
name='test'

# Information about the general task set
tasksinBkt = [5]

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6.]
hardTaskFactor = [wcetF2]
numDeadline = [1]

tasks=[]
keepsTasks=[]
numberOfRuns = 100
c_prob = []
seq_prob = []

for j in tasksinBkt:
    fileName = 'mp_tasks'+repr(j)+'_utilization'+repr(70)
    folder = 'comparison/'
    file = open(folder + 'txt/' +  fileName + '.txt', "w")
    file.write('Num of deadline miss: ' + repr(1) + '\n')
    file.write('Utilization: '+repr(70) + '\n')

    for i in range(numberOfRuns):
        print "Sample", i
        file.write('Generated '+ repr(j) +'samples:'+repr(i)+'\n')
        tasks=[]
        tasks=task_generator.taskGeneration_p(j,70)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, 10**-6.)
        keepsTasks=tasks[:]
        for k in tasks:
            file.write(repr(k) + ',')
            file.write('\n')

        #the following part is for testing
        file.write('DMP:\n')
        tdar = EPST.probabilisticTest_po(tasks, 3, 10)
        cpa = cprta.cprtao(keepsTasks)
        if tdar < cpa:
            file.write('bug?\n')

        file.write('EPST-K:\n')
        file.write(repr(tdar) + ',')
        file.write('\n')
        file.write('CPRTA:\n')
        file.write(repr(cpa) + ',')
        file.write('\n')
        c_prob.append(cpa)
        seq_prob.append(tdar)
        file.write('\n')

file.write('DMP:\n')
file.write('EPST-K:\n')
for i in seq_prob:
    file.write(repr(i) + ',')

file.write('\n')
file.write('CPRTA:\n')
for i in c_prob:
    file.write(repr(i) + ',')

file.write('\n')
file.close()
