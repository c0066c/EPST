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
#import edf_vd
#import rounded_mixed_task_builder

name='test'
stampEPST=[]
stampEPSTK=[]
stampCPRTA=[]

# Information about the general task set
#tasksinBkt = [5, 10, 20]
tasksinBkt = [5]
#tasksinBkt = [10]
#tasksinBkt = [5, 7, 10, 20, 30, 40]
#tasksinBkt = [5, 7, 10, 20]
#tasksinBkt = [20]

# Information about the mixed task set
#hardTaskPercentage = [100.0]
#wcetF1 = 1.3/1.2
wcetF2 = 2.2/1.2
wcetF3 = 3.4/1.2
wcetF4 = 1.7/1.4

#faultRate = [10**-12., 10**-10., 10**-17.]
#faultRate = [10**-4., 10**-5., 10**-6., 10**-7., 10**-8., 10**-9., 10**-10.]
#faultRate = [10**-6., 10**-7., 10**-8., 10**-9.]
faultRate = [10**-6.]
#toleratedRate = [10**-5., 10**-6., 10**-7.]
#toleratedRate = [10**-12.]

#hardTaskFactor = [wcetF4]
#hardTaskFactor = [wcetF4, wcetF2, wcetF3]
hardTaskFactor = [wcetF2]
#numDeadline = [1, 2, 3]
numDeadline = [1]
#hardTaskWCETFactor = 2.2/1.2
#softTaskWCETFactor = 2.2/1.2

tasks=[]
def func_star(a_b):
    """Covert 'f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call."""
#    print "once "
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
#            for percentageU in range(100, 101, 10):
                for fr in faultRate:
                    numberOfRuns = 1
                    print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(percentageU)
                    #for percentageU in range(45, 101, 1):
                    rel=[]
                    faultrel=[]
                    if __name__=='__main__':
                        freeze_support()
                        p = Pool(5)
                        a_arg = [1,1,1,1,1]
                        rel = (p.map(func_star, itertools.izip(a_arg, itertools.repeat(fr), itertools.repeat(tib))))
#                    for i in range(5):
#                        faultrel[len(faultrel):len(faultrel)]=rel[i]
                    print np.mean(stampCPRTA), '-', "avg time of CPRTA"
                    print np.mean(stampEPST), '-', "avg time of EPST"
                    print np.mean(stampEPSTK), '-', "avg time of EPSTK"
