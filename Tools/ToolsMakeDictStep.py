# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 01
# Modified : 2023 - 04 - 05

import pandas as pd
import numpy as np

def MakeDictStep(VerticalGrf, ApGrf):
    """
    This function make two dictionnary of the ground reaction force in vertical axes and
    anteroposterior axes with each step in index. Use a rolling median with a step size of 30 
    to smooth out data loss.

    Inputs: support phase vertical ground reaction force, support phase
        anteroposterior ground reaction force

    Outputs: Dictionnary of the vertical ground reaction force of each step, 
    Dictionnary of the anteroposterior ground reaction force of each step  
    """
    from Tools.ToolsGetStepEvent import GetStepEvent
    
    def RollingMedian(VerticalGrf, RollingMedianStep = 30):
        RollingMedianGrf = [abs(value) for value in VerticalGrf]
        RollingMedianGrf = pd.DataFrame(RollingMedianGrf)
        RollingMedianGrf = RollingMedianGrf.rolling(window = RollingMedianStep, center = True).median()
        RollingMedianGrf = RollingMedianGrf.fillna(0)
        RollingMedianGrf = RollingMedianGrf[0].tolist()
        return RollingMedianGrf
    
    # HeelStrike, ToeOff = GetStepEvent(RollingMedian(VerticalGrf)) # Si présence de NaN dans les data peut être utile
    HeelStrike, ToeOff = GetStepEvent(VerticalGrf)
    try :
        VerticalGrfStep = {i : VerticalGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike))}
        ApGrfStep = {i : ApGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike))} 
    except :
        VerticalGrfStep = {i : VerticalGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)} 
        ApGrfStep = {i : ApGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)} 

    return VerticalGrfStep, ApGrfStep

#def MakeDictStepForCut(VerticalGrf, ApGrf, RollingMedianStep = 30):
    """
    This function make two dictionnary of the ground reaction force in vertical axes and
    anteroposterior axes with each step in index. Use a rolling median with a step size of 30 
    to smooth out data loss.

    Inputs: support phase vertical ground reaction force, support phase
        anteroposterior ground reaction force

    Outputs: Dictionnary of the vertical ground reaction force of each step, 
    Dictionnary of the anteroposterior ground reaction force of each step  
    """

    def GetStepEvent(VerticalGrf):
        HeelStrike = []
        ToeOff = []
        for i in range(0,len(VerticalGrf)-1):
            if VerticalGrf[i] == 0 and VerticalGrf[i+1] > 0 : 
                HeelStrike.append(i)
            if VerticalGrf[i] > 0 and VerticalGrf[i+1] == 0 : 
                ToeOff.append(i)
        return HeelStrike, ToeOff
    
    def RollingMedian(VerticalGrf):
        RollingMedianGrf = [abs(value) for value in VerticalGrf]
        RollingMedianGrf = pd.DataFrame(RollingMedianGrf)
        RollingMedianGrf = RollingMedianGrf.rolling(window = RollingMedianStep, center = True).median()
        RollingMedianGrf = RollingMedianGrf.fillna(0)
        RollingMedianGrf = RollingMedianGrf[0].tolist()
        return RollingMedianGrf
    
    HeelStrike, ToeOff = GetStepEvent(RollingMedian(VerticalGrf))
    VerticalGrfStep = {i : VerticalGrf[HeelStrike[i]:ToeOff[i]] for i in range(0, len(HeelStrike))}
    ApGrfStep = {i : ApGrf[HeelStrike[i]:ToeOff[i]] for i in range(0, len(HeelStrike))}
    return VerticalGrfStep, ApGrfStep
