from __future__ import division
import random
import math
import time
import numpy as np
import sys, getopt
import matplotlib.pyplot as plt
from scipy.optimize import *
from sympy import *
import signal


def ft128dco(*args):
    A, B = map(np.float128, args)
    print A[0]*B[0]
    '''
    C = B[:]
    for i in A:
        for j in C:
            if i[0] == j[0]:
                j[1]=j[1]+i[1]
                i[0] = -1
    for i in A:
        if i[0] != -1:
            C.append(i)
    return C
    '''
A = np.array([1e-275], dtype='float128')
B = np.array([2.123e-200], dtype='float128')
C = np.array([1e-475], dtype='float128')
print A, B, np.float128(C[0])
D = [2.123e-200]
ft128dco(B,D)
print np.float128(1e-275)*np.float128(2.123e-200)
print 1e-275*2.123e-200

