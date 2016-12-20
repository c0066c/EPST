from multiprocessing import Pool, freeze_support
#import timing
import itertools
import random
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import tda
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
#import edf_vd
#import rounded_mixed_task_builder
name='test'

# Information about the general task set
#tasksinBkt = [5, 10, 20]
#tasksinBkt = [10]
tasksinBkt = [5, 10]

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
def insideroutine(numberOfRuns, fr):
    c_prob = []
    seq_prob = []
    for i in range(numberOfRuns):
        tasks=[]
        tasks=task_generator.taskGeneration_p(5,60)
        tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, fr)
        #the following part is for testing
        #c_prob.append(cprta.cprta(tasks))
        seq_prob.append(tda.probabilisticTest_p(tasks, 3, 3))
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
#                    for i in range(5):
#                        faultrel[len(faultrel):len(faultrel)]=rel[i]
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
'''
# plot in pdf
pp = PdfPages(folder + fileName + '.pdf')
title = 'ErrorRates: '+ repr(tib) + ', NumMisses:'+repr(fr) + ', Utilization:'+repr(percentageU)
plt.title(title, fontsize=20)
plt.grid(True)
if nd == 1:
    plt.ylabel('Maximum DMP', fontsize=24)
else:
    plt.ylabel('Maximum '+repr(nd)+'-consecutive DMP', fontsize=22)
plt.xlabel('n (# of tasks)', fontsize=22)
ax = plt.subplot()
ax.set_yscale("log")
ax.tick_params(axis='both', which='major',labelsize=20)
labels = ('CPRTA(5)','EPST-K(5)', 'CRPTA(10)','EPST-k(10)')
#TODO for comparision
#construct the box plot input
bxinput = []
for k,o in zip(cfault, perfault):
    bxinput.append(k)
    bxinput.append(o)
try:
    ax.boxplot(bxinput, 0, '', labels=labels)
except ValueError:
    print "ValueError"
pp.savefig()
plt.clf()
pp.close()
'''
