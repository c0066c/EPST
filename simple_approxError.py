from bounds import *
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
ErrorRate = [10**-6., 10**-7., 10**-8., 10**-9.]
tr = 10**-12.

hardTaskFactor = [wcetF2]
numDeadline = [1]
percentageU = 60
taskSet = []
def staticinput():
    global taskSet
    taskSet = []
    taskSet.append([{"execution": 0.4196494955752802, "deadline": 8.275927474938726, "period": 8.275927474938726}, {"execution": 4.054081876582606, "deadline": 59.27571879050128, "period": 59.27571879050128}, {"execution": 0.08191712223460931, "deadline": 8.324196589303817, "period": 8.324196589303817}, {"execution": 6.797674049325088, "deadline": 61.78761241440046, "period": 61.78761241440046}, {"execution": 0.23101492362748838, "deadline": 8.795363045434168, "period": 8.795363045434168}, {"execution": 2.6148922574888904, "deadline": 86.89916305347427, "period": 86.89916305347427}, {"execution": 0.6219709270104471, "deadline": 7.6343175719494365, "period": 7.6343175719494365}, {"execution": 0.5723991888219089, "deadline": 98.2638664448417, "period": 98.2638664448417}, {"execution": 0.1793135342154076, "deadline": 4.139193683991845, "period": 4.139193683991845}, {"execution": 12.075641598740901, "deadline": 69.37295296096302, "period": 69.37295296096302}])
    #task set 2
    #taskSet.append([{'execution': 0.5428921950482347, 'deadline': 8.802337496533735, 'period': 8.802337496533735}, {'execution': 3.4336497890308926, 'deadline': 35.750903307796406, 'period': 35.750903307796406}, {'execution': 0.9678759161459175, 'deadline': 8.369850936037853, 'period': 8.369850936037853}, {'execution': 2.0098581363339925, 'deadline': 31.82795192634464, 'period': 31.82795192634464}, {'execution': 0.019924949299748883, 'deadline': 8.080826123081218, 'period': 8.080826123081218}, {'execution': 1.5972567174172714, 'deadline': 73.45498471813272, 'period': 73.45498471813272}, {'execution': 0.5090611778884939, 'deadline': 9.930273572789957, 'period': 9.930273572789957}, {'execution': 2.0894012172807064, 'deadline': 80.88225762854599, 'period': 80.88225762854599}, {'execution': 0.1833081986400502, 'deadline': 5.110943593668344, 'period': 5.110943593668344}, {'execution': 6.298919576299053, 'deadline': 49.863995808351774, 'period': 49.863995808351774}])
    #task set 3
    #taskSet.append([{'execution': 0.16395341817575115, 'deadline': 1.8734696541496665, 'period': 1.8734696541496665}, {'execution': 0.3073938907649259, 'deadline': 25.547742259366434, 'period': 25.547742259366434}, {'execution': 0.6926060899480297, 'deadline': 8.364088966221166, 'period': 8.364088966221166}, {'execution': 0.34355838991294757, 'deadline': 39.104764430386325, 'period': 39.104764430386325}, {'execution': 0.039690741963806536, 'deadline': 5.529892879838412, 'period': 5.529892879838412}, {'execution': 5.600195265878802, 'deadline': 82.94657264893289, 'period': 82.94657264893289}, {'execution': 0.12949304877572035, 'deadline': 3.628303806055717, 'period': 3.628303806055717}, {'execution': 17.688666506150906, 'deadline': 92.7453323122661, 'period': 92.7453323122661}, {'execution': 0.43997346942016985, 'deadline': 9.236982066909885, 'period': 9.236982066909885}, {'execution': 3.191785643578826, 'deadline': 53.08643385034201, 'period': 53.08643385034201}])
    #task set 4
    #taskSet.append([{'execution': 0.20785279463209386, 'deadline': 4.5510483218574205, 'period': 4.5510483218574205}, {'execution': 0.2101562493203494, 'deadline': 96.59905003800424, 'period': 96.59905003800424}, {'execution': 0.2749912646222896, 'deadline': 3.2209964417585932, 'period': 3.2209964417585932}, {'execution': 2.9013449127260493, 'deadline': 57.05625702788033, 'period': 57.05625702788033}, {'execution': 0.016402726034014034, 'deadline': 3.0133449774736665, 'period': 3.0133449774736665}, {'execution': 5.466319291504701, 'deadline': 71.84116404095336, 'period': 71.84116404095336}, {'execution': 0.159104319608883, 'deadline': 7.4679044972957636, 'period': 7.4679044972957636}, {'execution': 2.7152814405072228, 'deadline': 56.11181213974435, 'period': 56.11181213974435}, {'execution': 0.35347257855241354, 'deadline': 5.95367015330951, 'period': 5.95367015330951}, {'execution': 3.720722880703234, 'deadline': 18.12075448781569, 'period': 18.12075448781569}])



keeptasks = taskSet[:]
for htf in hardTaskFactor:
    for nd in numDeadline:
        perError = []
        perError_dis = []
        for Er in ErrorRate:
            print('NumDeadline:'+repr(nd)+', FaultRate:'+repr(Er))
            probTask = []
            staticinput()
            print('Kpt:\n')
            for tasks in taskSet:
                tasks=mixed_task_builder.hardtaskWCET(tasks, htf, Er)
                resP = EPST.probabilisticTest_p(tasks, nd, Chernoff_bounds, 10)
                print resP
                probTask.append(resP) # get output probability from each task set // four task sets
            perError.append(probTask) # save the results per error rate

            probTask = []
            staticinput()
            #print taskSet
            print('Dpt:\n')
            for tasks in taskSet:
                tasks=mixed_task_builder.hardtaskWCET(tasks, htf, Er)
                resP = EPST.probabilisticTest_allp(tasks, nd, Chernoff_bounds, 10)
                probTask.append(resP) # get output probability from each task set // four task sets
                print resP
            perError_dis.append(probTask)
            #afterward, perfault list contains various faultRate results

        fileName = 'numMisses'+repr(nd)+'_utilization'+repr(percentageU)
        folder = 'fewcases/'

        file = open(folder + 'txt/' +  fileName + '.txt', "w")
        file.write('Num of deadline miss: ' + repr(nd) + '\n')
        file.write('Probability of deadline miss:\n')
        count = 0;
        file.write('Kpoints:'+'\n')
        for i in perError:
            file.write('Error Rate:'+repr(ErrorRate[count])+'\n')
            for j in i:
                file.write(repr(j) + ',')
            file.write('\n')
            file.write('\n')
        file.write('dispoints:'+'\n')
        for i in perError_dis:
            for j in i:
                file.write(repr(j) + ',')
            file.write('\n')
            file.write('\n')
            count+=1
        file.close()
