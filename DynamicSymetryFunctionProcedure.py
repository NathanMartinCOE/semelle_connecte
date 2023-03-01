# Dynamic Symetry Function (FSD) DynamicSymetryFunctionProcedure
# Author : Nathan Martin 
# Modified : 2023 - 03 - 01

import pandas as pd
import numpy as np


def DynamicSymetryFunctionProcedure(GrfValuesLeft, GrfValuesRight):
    """
    This function 

    Inputs: values of ground reaction force left get by GetGrfValues function, 
            values of ground reaction force right get by GetGrfValues function 

    Outputs: values of the Dynamic Symetry Function of each values for each step
    with value order as the "grf" function (FirtPeak, MidstanceValley, SecondPeak,FirtPeakTimeTo, 
    MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff, FirtAndMidstanceImpulse, 
    SecondAndPreswingImpulse, TotalVerticalGrfImpulse, BrakingPeak, PropulsivePeak, BrakePhaseDuration,
    PropulsivePhaseDuration, BrakePhaseTimeTo, PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse) 
    """
    DataFrameGrfValueLeft = pd.DataFrame(GrfValuesLeft).T
    DataFrameGrfValueRight = pd.DataFrame(GrfValuesRight).T
    DataFrameDynamicSymetryScore = pd.DataFrame(np.zeros(DataFrameGrfValueLeft.shape))

    def FSD(ligne, col):
        xdt = DataFrameGrfValueRight.iloc[ligne,col]
        xgt = DataFrameGrfValueLeft.iloc[ligne,col]
        if max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) == 0 :
                rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) + 1
        if max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) != 0 :
                rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col])  
        if max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) == 0 :
            rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) + 1
        if max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) != 0 :
            rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col])
        return 2*(xdt-xgt)/(rangexdt+rangexgt)

    for ligne in range(0,DataFrameGrfValueLeft.shape[0]):
        for col in range(0,DataFrameGrfValueLeft.shape[1]):
            DataFrameDynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)

    DataFrameDynamicSymetryScore = DataFrameDynamicSymetryScore.rename(columns={0:"FirtPeak", 1 : "MidstanceValley", 2 : "SecondPeak", 3 : "FirtPeakTimeTo", 
    4 : "MidstanceValleyTimeTo", 5 : "SecondPeakTimeTo", 6 : "TimeFromMidstanceValleyToToeOff", 7 : "FirtAndMidstanceImpulse", 8 :
    "SecondAndPreswingImpulse", 9 : "TotalVerticalGrfImpulse", 10 : "BrakingPeak", 11 : "PropulsivePeak", 12 : "BrakePhaseDuration", 13 :
    "PropulsivePhaseDuration", 14 : "BrakePhaseTimeTo", 15 : "PropulsivePhaseTimeTo", 16 : "BrakingImpulse", 17 : "PropulsiveImpulse"})

    return DataFrameDynamicSymetryScore