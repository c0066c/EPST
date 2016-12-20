import random
import timing
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
#import edf_vd
#import rounded_mixed_task_builder

name='test'

# Information about the general task set
#tasksinBkt = [5, 10, 20]
tasksinBkt = [10]
#tasksinBkt = [20]
#tasksinBkt = [30]
#tasksinBkt = [40]

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

for tib in tasksinBkt:
    for htf in hardTaskFactor:
        for nd in numDeadline:
            for percentageU in range(60, 61, 10):
                perfault = []
                for fr in faultRate:
                    numberOfRuns = 1
                    print('Tasks: ' + repr(tib) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(percentageU)
                    #for percentageU in range(45, 101, 1):
                    seq_prob = []
                    for i in range(numberOfRuns):
                        tasks=[]
                        tasks=task_generator.taskGeneration_p(tib,percentageU)
                        tasks=mixed_task_builder.hardtaskWCET(tasks, htf, fr)
                        keepTasks = tasks[:]
                        #the following part is for testing
                        timing.log("ptda method starts include opt")
                        resP = EPST.probabilisticTest_ptda(tasks, nd, 3)
                        timing.log("ptda method ends include opt")
                        timing.log("our method starts include opt")
                        resP = EPST.probabilisticTest_p(tasks, nd, 3)
                        timing.log("our method ends include opt")
                        seq_prob.append(resP) #this will get the maximum probability among the tasks in a task set.
                    perfault.append(seq_prob)
                    #afterward, perfault list contains various faultRate results
                fileName = 'tasks'+repr(tib)+'_numMisses'+repr(nd)+'_utilization'+repr(percentageU)
                folder = repr(numberOfRuns)+'/'
                file = open(folder + 'txt/' +  fileName + '.txt', "w")
                file.write('Runs: ' + repr(numberOfRuns) + '\n')
                file.write('Num of deadline miss: ' + repr(nd) + '\n')
                file.write('Utilization: '+repr(percentageU) + '\n')
                file.write('DMP:\n')
                count = 0;
                for i in perfault:
                    file.write('Fault Rate:'+repr(faultRate[count])+'\n')
                    for j in i:
                        file.write(repr(j) + ',')
                    file.write('\n')
                    file.write('\n')
                    count+=1
                file.close()
                lower_error=[]
                upper_error=[]
                median = []
                for i in range(len(perfault)):
                    median.append(np.median(perfault[i]))
                    lower_error.append(min(perfault[i]))
                    upper_error.append(max(perfault[i]))
                asymmetric_error = (lower_error, upper_error)
                print asymmetric_error

                # plot in pdf
                pp = PdfPages(folder + fileName + '.pdf')
                title = 'Tasks: '+ repr(tib) + ', NumMisses:'+repr(nd) + ', Utilization:'+repr(percentageU)
                plt.title(title, fontsize=24)
                plt.grid(True)
                if nd == 1:
                    plt.ylabel('Maximum DMP', fontsize=24)
                else:
                    plt.ylabel('Maximum '+repr(nd)+'-consecutive DMP', fontsize=22)
                plt.xlabel('Error rate', fontsize=22)
                ax = plt.subplot()
                ax.set_yscale("log", fontsize = 16)
                ind = np.arange(4)
                width = 0.4
                ax.set_xticks(ind + width + 0.2)
                labels = ('10^-6','10^-7', '10^-8','10^-9')
                try:
                    ax.boxplot(perfault, 0, '', labels=labels)
                except ValueError:
                    print "ValueError"
                pp.savefig()
                plt.clf()
                pp.close()

