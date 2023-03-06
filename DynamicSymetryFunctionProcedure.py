# Dynamic Symetry Function (FSD) DynamicSymetryFunctionProcedure
# Author : Nathan Martin 
# Modified : 2023 - 03 - 01

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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


def PlotDynamicSymetryFunction(VerticalGrfRight, VerticalGrfLeft):
    XVerticalGrfRight = np.linspace(0,len(VerticalGrfRight),len(VerticalGrfRight))
    XVerticalGrfLeft = np.linspace(0,len(VerticalGrfLeft),len(VerticalGrfLeft))
    
    LenMinGrf = min([len(VerticalGrfRight),len(VerticalGrfLeft)])
    #ValueMaxGrf = max([max(VerticalGrfRight),max(VerticalGrfLeft)])
    #Thresfold = ValueMaxGrf * 5 / 100
    Thresfold = 5 / 100

    DataFrameVerticalGrfRight = pd.DataFrame({'xRight':XVerticalGrfRight,'yRight':VerticalGrfRight})
    DataFrameVerticalGrfLeft = pd.DataFrame({'xLeft':XVerticalGrfLeft,'yLeft':VerticalGrfLeft})
    DataFrameVerticalGrfRight['xnormRight'] = DataFrameVerticalGrfRight['xRight'] * 100 / DataFrameVerticalGrfRight['xRight'][len(DataFrameVerticalGrfRight)-1]
    DataFrameVerticalGrfLeft['xnormLeft']=DataFrameVerticalGrfLeft['xLeft'] * 100 / DataFrameVerticalGrfLeft['xLeft'][len(DataFrameVerticalGrfLeft)-1]

    ThresfoldPositive = [Thresfold] * LenMinGrf
    ThresfoldNegative = [-Thresfold] * LenMinGrf
    xdt = DataFrameVerticalGrfRight['yRight']
    xgt = DataFrameVerticalGrfLeft['yLeft']
    VerticalGrfAsym = []
    conditionfillpositive = []
    conditionfillnegative = []
    rangexdt = max(xdt) - min(xdt)
    rangexgt = max(xgt) - min(xgt)
    for i in range(0, LenMinGrf):
        VerticalGrfAsym.append(2*(xdt[i]-xgt[i])/(rangexdt+rangexgt) * 100)
        conditionfillpositive.append(VerticalGrfAsym[i] >= ThresfoldPositive[i])
        conditionfillnegative.append(VerticalGrfAsym[i] <= ThresfoldNegative[i])

    plt.figure(figsize=(15,8))
    plt.plot(DataFrameVerticalGrfRight['xnormRight'], DataFrameVerticalGrfRight['yRight'], c='b', ls='--', label='Jambe gauche')
    plt.plot(DataFrameVerticalGrfLeft['xnormLeft'], DataFrameVerticalGrfLeft['yLeft'], c='r', ls='--', label='Jambe droite')
    plt.plot(DataFrameVerticalGrfRight['xnormRight'], VerticalGrfAsym, c='black', label = 'Fonction de Symétrie Dynamique')
    plt.hlines(y = Thresfold, xmin=0, xmax = max(DataFrameVerticalGrfRight['xnormRight']), colors='black',
                lw=0.5, ls='--', label = f'5% Thresfold (={Thresfold})')
    plt.hlines(y = -Thresfold, xmin=0, xmax = max(DataFrameVerticalGrfRight['xnormRight']), colors='black',
                lw=0.5, ls='--', label = f'-5% Thresfold (={-Thresfold})')
    plt.fill_between(x = DataFrameVerticalGrfRight['xnormRight'], y1 = ThresfoldPositive, y2 = VerticalGrfAsym, where = conditionfillpositive, alpha = 0.2, color = 'r')
    plt.fill_between(x = DataFrameVerticalGrfRight['xnormRight'], y1 = ThresfoldNegative, y2 = VerticalGrfAsym, where = conditionfillnegative, alpha = 0.2, color = 'r')
    plt.legend()
    plt.show()