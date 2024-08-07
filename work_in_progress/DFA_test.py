# test Detrended Fluctuation Analysis

import numpy as np
import matplotlib.pyplot as plt

import fathon
from fathon import fathonUtils as fu

#time series
a = np.random.randn(10000)

#zero-mean cumulative sum
a = fu.toAggregated(a)

#initialize dfa object
pydfa = fathon.DFA(a)

#compute fluctuation function and Hurst exponent
wins = fu.linRangeByStep(10, 2000)
n, F = pydfa.computeFlucVec(wins, revSeg=True, polOrd=3)
H, H_intercept = pydfa.fitFlucVec()

#compute Hurst exponent in different ranges
limits_list = np.array([[15,2000], [200,1000]], dtype=int)
list_H, list_H_intercept = pydfa.multiFitFlucVec(limits_list)


import ipdb; ipdb.set_trace()
plt.figure()
plt.plot(a)
plt.show()