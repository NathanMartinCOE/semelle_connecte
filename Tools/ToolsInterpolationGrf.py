# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 04 - 07

import numpy as np
from scipy import interpolate


def InterpolationGrf(Grf):
    """ This function normalized Ground Reaction force step in % of cycle by
    interpolated

    Agrs: 
        Grf: Ground Reaction Force of one step

    Output: 
        xnew: new indice can be used for plot
        ynew: new Ground Reaction force normalised in % of cycle
    """
    x = np.linspace(0,len(Grf),len(Grf))
    y = Grf
    f = interpolate.interp1d(x, y)
    xnew = np.linspace(0, len(Grf), 100)
    ynew = f(xnew)

    return xnew, ynew


def Interpolation(data, xnew_num = 100):
    """ This function normalized Ground Reaction force step in % of cycle by
    interpolated

    Agrs: 
        Grf: Ground Reaction Force of one step
        xnew_num (int): to select the number of interpolation points

    Output: 
        xnew: new indice can be used for plot
        ynew: new Ground Reaction force normalised in % of cycle
    """
    x = np.linspace(0,len(data),len(data))
    y = data
    f = interpolate.interp1d(x, y)
    xnew = np.linspace(0, len(data), xnew_num)
    ynew = f(xnew)

    return xnew, ynew