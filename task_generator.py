'''
Author Kevin Huang and Georg von der Brueggen

'''

from __future__ import division
import random
import math
import numpy
import sys, getopt
import json

ofile = "taskset-p.txt"
USet=[]

def UUniFast(n,U_avg):
	global USet
	sumU=U_avg
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))
		USet.append(sumU-nextSumU)
		sumU=nextSumU
	USet.append(sumU)

def UUniFast_Discard(n,U_avg):
	while 1:
		sumU=U_avg
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))
			USet.append(sumU-nextSumU)
			sumU=nextSumU
		USet.append(sumU)

		if max(USet) < 1:
			break
		del USet[:]

def UniDist(n,U_min,U_max):
	for i in range(n-1):
		uBkt=random.uniform(U_min, U_max)
		USet.append(uBkt)

def CSet_generate(Pmin,numLog):
	global USet,PSet
	j=0
	for i in USet:
		thN=j%numLog
		#p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
		p=random.uniform(1, 50)
		pair={}
		pair['period']=p
		pair['deadline']=p#*random.uniform(1)
		pair['execution']=i*p
		PSet.append(pair)
		j=j+1;

def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration_p(numTasks,uTotal):
	random.seed()
	init()
	UUniFast(numTasks,uTotal/100)

	CSet_generate(1,2)
        fo = open(ofile, "ab")
        print >>fo, json.dumps(PSet)
	return PSet

print taskGeneration_p(20, 60)
