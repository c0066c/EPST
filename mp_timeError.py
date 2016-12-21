from multiprocessing import Pool, freeze_support
import itertools
import random
import timing
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import EPST
import cprta
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages

name='test'
stampEPST=[]
stampEPSTK=[]
stampCPRTA=[]

# Information about the general task set
tasksinBkt = [5]

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6.]
hardTaskFactor = [wcetF2]
numDeadline = [1]

tasks=[]
def func_star(a_b):
    """Covert 'f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call."""
    return insideroutine(*a_b)

def insideroutine(numberOfRuns, fr, tib):
    seq_prob = []
    for i in range(numberOfRuns):
        tasks=[]
        tasks=task_generator.taskGeneration_p(tib,60)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
        keepTasks = tasks[:]
        #the following part is for testing
        timing.tlog_start("CPRTA starts", 0 )
        resEPSTK = cprta.cprta(tasks)
        timing.tlog_end("CPRTA ends", stampCPRTA, 0)

        timing.tlog_start("EPST method starts", 0)
        resEPST = EPST.probabilisticTest_ptda_pt(tasks, nd, 3) #no opt
        timing.tlog_end("EPST method ends", stampEPST, 0)

        timing.tlog_start("EPSTK starts", 0 )
        resEPSTK = EPST.probabilisticTest_pt(tasks, nd, 3) #no opt
        timing.tlog_end("EPSTK ends", stampEPSTK, 0)

    return seq_prob
for tib in tasksinBkt:
    for htf in hardTaskFactor:
        for nd in numDeadline:
            for percentageU in range(60, 61, 10):
                for fr in faultRate:
                    numberOfRuns = 1
                    print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(percentageU)                    
                    rel=[]
                    faultrel=[]
                    if __name__=='__main__':
                        freeze_support()
                        p = Pool(5)
                        a_arg = [1,1,1,1,1]
                        rel = (p.map(func_star, itertools.izip(a_arg, itertools.repeat(fr), itertools.repeat(tib))))

                    print np.mean(stampCPRTA), '-', "avg time of CPRTA"
                    print np.mean(stampEPST), '-', "avg time of EPST"
                    print np.mean(stampEPSTK), '-', "avg time of EPSTK"
