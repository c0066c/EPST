import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
#import edf_vd
#import rounded_mixed_task_builder
name='test'

# Information about the general task set
tasksinBkt = [10]

# Information about the mixed task set
wcetF2 = 2.2/1.2
wcetF3 = 3.4/1.2
wcetF4 = 1.7/1.4

faultRate = [10**-6.]

hardTaskFactor = [wcetF2]
numDeadline = [1]

numberOfRuns = 100

fileName = 'mp_tasks'+repr(10)+'_utilization'+repr(60)+'_'+repr(70)
folder = 'comparison/'

# plot in pdf
pp = PdfPages(folder + fileName + '.pdf')
title = 'Tasks: '+repr(10)+', FaultRate: '+ repr(10**-6.) + ', NumMisses: '+repr(1)
plt.title(title, fontsize=20)
plt.grid(True)
plt.ylabel('Calculated DMP', fontsize=20)
#plt.xlabel('Approaches($U^*$)', fontsize=20)
ax = plt.subplot()
ax.set_yscale("log")
ax.set_ylim([10**-100,10**19])
ax.tick_params(axis='both', which='major',labelsize=16)

'''
box = mpatches.Patch(color='blue', label='First to Third Quartiles', linewidth=3)
av = mpatches.Patch(color='red', label='Median', linewidth=3)
whisk = mpatches.Patch(color='black', label='Whiskers', linewidth=3)
plt.legend(handles=[utilization], fontsize=12, frameon=True, loc=3)
'''

labels = ('CPRTA-resample','Chernoff-K', 'CPRTA-resample','Chernoff-K')
#construct the box plot input
bxinput = []
#utilization 60%
c_prob = [1,1,1,1,1,1,5.00E-18,1.00E-42,1,1,1,1,1.46E-34,1,1,1.00E-18,1.00E-24,1,1,1,1,1.00E-12,1,1.00E-06,1,2.00E-18,1,5.24E-94,3.00E-18,5.00E-30,3.00E-12,1,1,1,1,3.00E-24,1,1.00E-18,1,3.70E-29,1,1,2.00E-30,1,1,2.70E-41,1,6.00E-12,1,9.27E-58,1,1,1,1,1,1,1,1,1.10E-41,9.00E-30,1.20E-23,1,1,1,3.00E-30,1,1,2.00E-24,1,6.00E-30,1.00E-06,1,1,1,1,2.00E-48,1.00E-24,1,1,1,1,3.00E-24,1,1.00E-42,1,1.75E-69,1,1,3.00E-24,1,2.47E-46,1.57E-52,3.00E-60,3.40E-29,1,4.00E-30,2.10E-29,1,1,1]
seq_prob = [6.69639168165574e-20, 2.66467713798493e-19, 1.63009255999164e-18, 7.00869162953942e-28, 7.71640544378684e-10, 1.46925771330277e-13, 3.49321101849714e-18, 1.49121060354920e-25, 7.14500241521163e-19, 6.26824235856911e-16, 3.21902355090564e-21, 1.78106545604155e-21, 1.58097996679526e-23, 1.15901529033325e-20, 6.18801747852360e-28, 1.00043360639702e-24, 2.35216458545530e-25, 2.35811839973435e-25, 1.17715664589658e-29, 2.41210207200242e-13, 8.17502216583052e-22, 2.44923363398518e-28, 2.32010857502311e-31, 1.21717353716265e-27, 5.80252003072423e-33, 3.90131366544063e-17, 1.34006999028697e-29, 1.83280579870670e-20, 3.08689037859798e-16, 7.84489800142876e-28, 4.46431412038633e-15, 1.01102368193402e-24, 1.89315114089426e-13, 7.21012831168176e-25, 2.32655784082685e-25, 1.86143143844230e-10, 6.85335402431681e-24, 2.99196996542327e-16, 9.09536569606743e-14, 3.54461298859058e-24, 6.78538206091318e-14, 7.57574812359143e-23, 3.91713324572261e-22, 1.28224112800926e-31, 2.14349061712092e-23, 2.54856580010919e-30, 3.66878529552725e-26, 6.04582146509656e-22, 2.25298676430388e-18, 3.24326771554419e-30, 1.08969511060901e-11, 1.67563474503851e-19, 6.96903230981814e-24, 5.56506578063617e-15, 2.45536374708809e-14, 2.20657245566057e-28, 4.62169903218462e-20, 1.77087044091953e-20, 9.46867960564462e-18, 3.93125174473780e-27, 1.37156109363511e-20, 1.09522205950303e-19, 2.00269910488445e-17, 1.91306970033569e-14, 8.72778776151902e-25, 7.77924369318895e-16, 1.56054248914707e-20, 9.82608351306544e-25, 4.28757330357830e-22, 4.33943614808367e-20, 2.44824963059736e-21, 1.37762985441810e-14, 3.49197160559660e-19, 6.57612003444995e-20, 1.29228502165152e-24, 4.22461542081251e-19, 4.35386769835130e-24, 4.71938659395318e-12, 4.66665906601756e-22, 8.80094931426111e-23, 8.48682465235082e-18, 6.02923413040210e-25, 1.62150565774923e-21, 8.18167611054630e-30, 2.81969170475222e-13, 1.53560973683770e-23, 5.73670669917385e-24, 6.01204171569722e-21, 5.25309259487166e-23, 1.82437999985983e-16, 2.04421670182695e-32, 1.04837110466136e-13, 8.53788835775924e-24, 1.80468816196437e-18, 1.29047778878436e-29, 3.33060113307284e-27, 3.58286479745769e-26, 3.02012192329108e-12, 1.42060623630094e-29, 3.28055981687886e-27]
bxinput.append(c_prob)
bxinput.append(seq_prob)

#utilization 70%
c_prob = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1.00E-06,1,1,5.00E-12,1,1,1.00E-06,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
seq_prob = [6.03415306537333e-15, 2.46679111943179e-8, 1.92656222894609e-5, 6.08751390397739e-15, 1.38354597320023e-6, 2.94982224072812e-10, 1.84906972852323e-9, 0.000114133108691848, 3.14527496993744e-17, 3.31183271489768e-14, 1.07126209066059e-7, 4.48820240673834e-15, 0.000670257713134885, 1.17842840836547e-6, 2.04580495023485e-10, 2.82114945761372e-5, 7.90788217983615e-11, 2.17630681777749e-15, 4.38025658396812e-7, 2.82780198723551e-11, 5.57357804775770e-14, 8.43151946423062e-11, 4.35182582049801e-7, 8.65032201492064e-8, 4.14552732823657e-13, 6.18520707162773e-13, 3.57350207565078e-9, 3.18924460529162e-15, 3.52303560555710e-6, 9.51726662504310e-13, 1.44980766568351e-5, 5.25602198666655e-5, 3.10367287068853e-7, 4.79233360144337e-7, 1.08084128816128e-13, 6.44242112734386e-10, 1.53153275832339e-14, 1.76865683106478e-15, 1.05194497580332e-7, 1.40376990451831e-7, 2.84165192357385e-9, 0.000270308290018625, 5.70151787865316e-5, 3.03897612149033e-8, 5.70884848344953e-6, 1.46473017800673e-10, 4.51332333663833e-12, 5.92614287649164e-16, 1.89018233781586e-5, 1.45434521327311e-15, 1.01747102839943e-16, 1.38286990706073e-7, 2.73781906462916e-10, 8.86328695254472e-6, 3.34947283471758e-6, 5.72167364409255e-17, 1.76062238110757e-5, 3.92092816452726e-12, 8.47150095833604e-10, 1.49259035519367e-7, 1.42363234846727e-7, 1.80798774094175e-13, 4.90728695861547e-10, 1.15140987016836e-15, 7.18313302325152e-6, 0.000769375445103534, 7.55277041371715e-18, 1.62800317904405e-5, 2.07901409705283e-17, 2.10313514039352e-9, 1.04497978181781e-16, 0.000186736868198147, 5.24291566392148e-18, 6.19518783935512e-9, 1.18455271499490e-5, 4.88166482430324e-10, 8.62047450175126e-15, 1.14772985064022e-13, 1.29617123914589e-19, 1.86208317645631e-5, 2.20033713709603e-12, 1.38358295500432e-11, 1.18206447637519e-12, 1.25135515912444e-9, 3.80191391141082e-9, 2.23822534194847e-17, 5.09680576699871e-7, 0.00116817732765849, 5.78166539481946e-10, 0.000662914302704798, 1.25208721509397e-12, 1.83201469169950e-6, 8.85107425440668e-15, 1.09508569844934e-19, 4.57262511238418e-8, 1.49474326170200e-5, 6.47489242329793e-15, 9.27220047998907e-8, 1.44474035126556e-7, 2.38072230013344e-5]
bxinput.append(c_prob)
bxinput.append(seq_prob)

#the blue box
boxprops = dict(linewidth=2, color='blue')
#the median line
medianprops = dict(linewidth=2.5, color='red')
whiskerprops = dict(linewidth=2.5, color='black')
capprops = dict(linewidth=2.5)


try:
    ax.boxplot(bxinput, 0, '', labels=labels, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops, medianprops=medianprops)
except ValueError:
    print "ValueError"

ax.vlines(0.5, 0, 1, transform=ax.transAxes )
ax.text(0.32, 0.04, "$U_{sum}^N=60\%$", transform=ax.transAxes, size=16 )
ax.text(0.82, 0.04, "$U_{sum}^N=70\%$", transform=ax.transAxes, size=16 )

figure = plt.gcf()
figure.set_size_inches([10, 4])

box = mpatches.Patch(color='blue', label='First to Third Quartiles', linewidth=3)
av = mpatches.Patch(color='red', label='Median', linewidth=3)
whisk = mpatches.Patch(color='black', label='Whiskers', linewidth=3)

plt.legend(handles=[av, box, whisk], fontsize=12, frameon=True, loc=5)


pp.savefig()
plt.clf()
pp.close()

