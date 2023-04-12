# Procedure GroundReactionForce grf
#Author: Nathan Martin 2023-02-28

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

def grf(VerticalGrf,ApGrf,FrameRate = 10):

    """
    This function quantifies variables related to vertical and anteroposterior
    ground reaction forces during walking. Impulses are found by integrating the 
    force curve with respect to time. This script assumes that the vertical force 
    is positive, the anteroposterior braking force is negative, the anteroposterior 
    propulsive force is positive.

    Inputs: support phase vertical ground reaction force, support phase
        anteroposterior ground reaction force, frame rate

    Outputs: 
        (VERTICAL GRF) :
            Peak : FirtPeak, MidstanceValley, SecondPeak,
            Time to : FirtPeakTimeTo, MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff,
            Impulse : FirtAndMidstanceImpulse, SecondAndPreswingImpulse, TotalVerticalGrfImpulse,
        (ANTPOST GRF) :
            Peak : BrakingPeak, PropulsivePeak, BrakePhaseDuration,
            Duration : PropulsivePhaseDuration,
            Time to : BrakePhaseTimeTo,
            Impulse : PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse
    """
    # Function for change dtype to list
    def ToList(data):
        if type(data) == list:
            pass
        elif type(data) == np.ndarray:
            data = list(data)
        elif type(data) == pd.core.series.Series:
            data = data.to_list()
        return data
    
    VerticalGrf = ToList(VerticalGrf)
    ApGrf = ToList(ApGrf)
    TabVGrf = np.array(VerticalGrf)

    #Index
    FirtPeakIndex = argrelextrema(TabVGrf, np.greater)[0][0]
    MidstanceValleyIndex = argrelextrema(TabVGrf, np.less)[0][0]
    SecondPeakIndex = argrelextrema(TabVGrf, np.greater)[0][1]

    #Peak
    FirtPeak = VerticalGrf[FirtPeakIndex]
    MidstanceValley = VerticalGrf[MidstanceValleyIndex]
    SecondPeak = VerticalGrf[SecondPeakIndex]

    #Time to ..
    FirtPeakTimeTo = len(VerticalGrf[ :FirtPeakIndex])/FrameRate
    MidstanceValleyTimeTo = len(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
    SecondPeakTimeTo = len(VerticalGrf[ :SecondPeakIndex])/FrameRate
    TimeFromMidstanceValleyToToeOff = len(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
    
    #Impulse
    FirtAndMidstanceImpulse = np.trapz(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
    SecondAndPreswingImpulse = np.trapz(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
    TotalVerticalGrfImpulse = np.trapz(VerticalGrf)/FrameRate

    """
    ----------- ANTEROPOSTERIOR GRFS -----------
    """

    #Index
    ApGrfIndexBrakingPeak = ApGrf.index(min(ApGrf))
    ApGrfIndexPropulsivePeak = ApGrf.index(max(ApGrf))
    ApGrfPower = [grf ** 2 for grf in ApGrf[ApGrfIndexBrakingPeak : ApGrfIndexPropulsivePeak]]
    ApGrfIndexZero = ApGrfIndexBrakingPeak + ApGrfPower.index(min(ApGrfPower))

    #Peak 
    BrakingPeak = min(ApGrf)
    PropulsivePeak = max(ApGrf)

    #Duration
    BrakePhaseDuration = len(ApGrf[ :ApGrfIndexZero])/FrameRate
    PropulsivePhaseDuration = len(ApGrf[ApGrfIndexZero: ])/FrameRate
    
    #Time to ..
    BrakePhaseTimeTo = len(ApGrf[ :ApGrfIndexBrakingPeak])/FrameRate
    PropulsivePhaseTimeTo = len(ApGrf[ApGrfIndexZero:ApGrfIndexPropulsivePeak])/FrameRate

    #Impulse
    BrakingImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue < 0])/FrameRate
    PropulsiveImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue > 0])/FrameRate

    return FirtPeak, MidstanceValley, SecondPeak, FirtPeakTimeTo, MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff, FirtAndMidstanceImpulse, SecondAndPreswingImpulse, TotalVerticalGrfImpulse, BrakingPeak, PropulsivePeak, BrakePhaseDuration, PropulsivePhaseDuration, BrakePhaseTimeTo, PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse
