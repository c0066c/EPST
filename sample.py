import itertools
import random
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import EPST
from bounds import *

# Information about the general task set
tasksinBkt = [5]

# Information about the number of testing runs
numberOfRuns = 1

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6.]
hardTaskFactor = [wcetF2]
numDeadline = [1]

tasks=[]
for j in tasksinBkt:
    for tib in tasksinBkt:
        for fr in faultRate:
            print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(1)+', FaultRate:'+repr(10**-6.)+', Utilization:'+repr(60))
            seq_prob = []
            for i in range(numberOfRuns):
                tasks=[]
                tasks=task_generator.taskGeneration_p(j,60)
                tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
                #print tasks
                #the following part is for testing
                seq_prob.append(EPST.probabilisticTest_p(tasks, 1, Chernoff_bounds, 1))
                seq_prob.append(EPST.probabilisticTest_p(tasks, 1, Hoeffding_inequality))
                seq_prob.append(EPST.probabilisticTest_p(tasks, 1, Bernstein_inequality))
            print seq_prob
