import random
import timing
import math
import numpy as np
#import task_generator
import mixed_task_builder
import sort_task_set
import EPST
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
import ast

name='test'

# Information about the mixed task set
faultRate = [10**-6.]
hardTaskFactor = [1.83]
numDeadline = [1]

tasks=[]


for htf in hardTaskFactor:
    for nd in numDeadline:
        perfault = []
        for fr in faultRate:
            print('Tasks: ' + repr(10) +', NumDeadline:'+repr(nd)+', FaultRate:'+repr(fr))+', Utilization:'+repr(60)
            seq_prob = []
            tasks=[]

            #read from given input
            ifile = "taskset-p.txt"
            s = open(ifile, "rb").read()
            tasks = ast.literal_eval(s)

            keepTasks = tasks[:]
            #the following part is for testing
            #timing.log("ptda method starts include opt")
            #resP = EPST.probabilisticTest_ptda(tasks, nd, 3)
            #timing.log("ptda method ends include opt")
            timing.log("our method starts include opt")
            resP = EPST.probabilisticTest_p(tasks, nd, 20)
            timing.log("our method ends include opt")
            #this will get the maximum probability among the tasks in a task set.
            print resP
'''
        fileName = 'tasks'+repr(5)+'_numMisses'+repr(nd)+'_utilization'+repr(60)
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
'''
'''
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
'''
