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
tasksinBkt = [10]

# Information about the mixed task set
wcetF2 = 2.2/1.2
wcetF3 = 3.4/1.2
wcetF4 = 1.7/1.4

faultRate = [10**-6.]

hardTaskFactor = [wcetF2]
numDeadline = [1]

tasks=[]

for tib in tasksinBkt:
    fileName = 'time_mp_tasks'+repr(tib)+'_utilization'+repr(60)
    folder = 'comparison/'
    file = open(folder + 'txt/' +  fileName + '.txt', "w")
    file.write('Num of deadline miss: ' + repr(1) + '\n')
    file.write('Utilization: '+repr(60) + '\n')

    for htf in hardTaskFactor:
        for nd in numDeadline:
            for percentageU in range(60, 61, 10):
            #for percentageU in range(10, 11, 10):
#            for percentageU in range(30, 31, 10):
#            for percentageU in range(100, 101, 10):
                for fr in faultRate:
                    numberOfRuns = 500
                    print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(percentageU)
                    for i in range(numberOfRuns):
                        print "sample: ", i
                        file.write('Generated '+ repr(tib) +'samples:'+repr(i)+'\n')
                        tasks=[]
                        tasks=task_generator.taskGeneration_p(tib,percentageU)
                        tasks=mixed_task_builder.hardtaskWCET(tasks, htf, fr)
                        keepTasks = tasks[:]
                        for k in tasks:
                            file.write(repr(k) + ',')
                            file.write('\n')

                        #the following part is for testing

                        timing.tlog_start("CPRTA starts", 1)
#                        resEPSTK = cprta.cprtao(tasks)
                        timing.tlog_end("CPRTA ends", stampCPRTA, 1)

                        if len(stampCPRTA) > 0:
                            file.write('Duration: '+repr(stampCPRTA[-1])+'\n')

                        tasks = keepTasks[:]
                        timing.tlog_start("EPST method starts", 0)
                        resEPST = EPST.probabilisticTest_ptda_pt(tasks, nd, 3) #no opt
                        timing.tlog_end("EPST method ends", stampEPST, 0)
                        if len(stampEPST) > 0:
                            file.write('Duration: '+repr(stampEPST[-1])+'\n')

                        tasks = keepTasks[:]
                        timing.tlog_start("EPSTK starts", 0 )
                        resEPSTK = EPST.probabilisticTest_pt(tasks, nd, 3) #no opt
                        timing.tlog_end("EPSTK ends", stampEPSTK, 0)
                        if len(stampEPSTK) > 0:
                            file.write('Duration: '+repr(stampEPSTK[-1])+'\n')

                        print np.mean(stampCPRTA), '-', "avg time of CPRTA"
                        print "skip times (over 10mins):",cprta.reportSkipTimes()
                        print np.mean(stampEPST), '-', "avg time of EPST"
                        print np.mean(stampEPSTK), '-', "avg time of EPSTK"
#                    for y,j,k in zip(stampCPRTA, stampEPST, stampEPSTK):
#                        print timing.secondsToStr(y)
                    file.write("Total result:\n")
                    file.write(repr(np.mean(stampCPRTA))+'-'+"avg time of CPRTA\n")
                    file.write("skip times (over 10mins):"+repr(cprta.reportSkipTimes())+'\n')
                    file.write(repr(np.mean(stampEPST))+'-'+"avg time of EPST\n")
                    file.write(repr(np.mean(stampEPSTK))+'-'+"avg time of EPSTK\n")
    file.close()
