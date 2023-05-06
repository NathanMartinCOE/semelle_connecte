# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 04 - 07

""" This function normalized any Ground Reaction force step in % of cycle by
    interpolated

    Agrs: Ground Reaction Force of one step

    Output: 
        new x value : for plot
        new y value : Ground Reaction force normalised in % of cycle
"""

import numpy as np
from scipy import interpolate


def InterpolationGrf(Grf):
    x = np.linspace(0,len(Grf),len(Grf))
    y = Grf
    f = interpolate.interp1d(x, y)
    xnew = np.linspace(0, len(Grf), 100)
    ynew = f(xnew)
    return xnew, ynew


def Interpolation(data, xnew_num = 100):
    x = np.linspace(0,len(data),len(data))
    y = data
    f = interpolate.interp1d(x, y)
    xnew = np.linspace(0, len(data), xnew_num)
    ynew = f(xnew)
    return xnew, ynew