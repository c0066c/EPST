from multiprocessing import Pool, freeze_support
import itertools
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
tasksinBkt = [10]

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6., 10**-7., 10**-8., 10**-9.]
hardTaskFactor = [wcetF2]
numDeadline = [3]

tasks=[]
def func_star(a_b):
    """Covert 'f([a,b,c,d,e,f]) to f(a,b,c,d,e,f) call."""
    return insideroutine(*a_b)

def insideroutine(numberOfRuns, fr):
    seq_prob = []
    for i in range(numberOfRuns):
        tasks=[]
        tasks=task_generator.taskGeneration_p(10,60)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
        keepTasks = tasks[:]
        #the following part is for testing
        resP = EPST.probabilisticTest_p(tasks, 3, 3)
        seq_prob.append(resP) #this will get the maximum probability among the tasks in a task set.
    return seq_prob

for tib in tasksinBkt:
    for htf in hardTaskFactor:
        for nd in numDeadline:
            for percentageU in range(60, 61, 10):
                perfault = []
                for fr in faultRate:
                    numberOfRuns = 500
                    print('Runs: ' + repr(numberOfRuns) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(percentageU)
                    rel=[]
                    faultrel=[]
                    if __name__=='__main__':
                        freeze_support()
                        p = Pool(5)
                        a_arg = [100,100,100,100,100]
                        rel = (p.map(func_star, itertools.izip(a_arg, itertools.repeat(fr))))
                    for i in range(5):
                        faultrel[len(faultrel):len(faultrel)]=rel[i]
                    perfault.append(faultrel)
                fileName = 'mp_runs'+repr(numberOfRuns)+'_numMisses'+repr(nd)+'_utilization'+repr(percentageU)
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
                for i in range(4):
                    median.append(np.median(perfault[i]))
                    lower_error.append(min(perfault[i]))
                    upper_error.append(max(perfault[i]))
                asymmetric_error = (lower_error, upper_error)
                print asymmetric_error

                # plot in pdf
                pp = PdfPages(folder + fileName + '.pdf')
                title = 'Runs: '+ repr(numberOfRuns) + ', NumMisses:'+repr(nd) + ', Utilization:'+repr(percentageU)
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

