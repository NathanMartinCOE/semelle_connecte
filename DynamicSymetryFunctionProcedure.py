# Dynamic Symetry Function (FSD) DynamicSymetryFunctionProcedure
# Author : Nathan Martin 
# Modified : 2023 - 03 - 01

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


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


def PlotDynamicSymetryFunctionRealtime(VerticalGrfRight, VerticalGrfLeft):    


    # Rajoute des 0 après le pas le plus court en temps
    if VerticalGrfRight.shape[0] > VerticalGrfLeft.shape[0]:
        AddZero = [0] * (VerticalGrfRight.shape[0]-VerticalGrfLeft.shape[0])
        VerticalGrfLeft = np.concatenate((VerticalGrfLeft, AddZero))
    elif VerticalGrfLeft.shape[0] > VerticalGrfRight.shape[0]:
        AddZero = [0] * (VerticalGrfLeft.shape[0]-VerticalGrfRight.shape[0])
        VerticalGrfRight = np.concatenate((VerticalGrfRight, AddZero))

    # Definition d'un thresfold de 5/100 et de -5/100 pour la FSD
    Thresfold = 5/100
    ThresfoldPositive = [Thresfold] * max([VerticalGrfRight.shape[0], VerticalGrfLeft.shape[0]])
    ThresfoldNegative = [-Thresfold] * max([VerticalGrfRight.shape[0], VerticalGrfLeft.shape[0]])

    # Création d'un DataFrame contenant les forces de réactions au sol de la jambe droite et gauche
            # et des Thresfold positif et négatif
    DataFrameVerticalGrf = pd.DataFrame({'yRight': VerticalGrfRight,
                                         'yLeft': VerticalGrfLeft,
                                         'ThresfoldPositive': ThresfoldPositive,
                                          'ThresfoldNegative' : ThresfoldNegative})
    
    # Calcul de la fonction de symetrie dynamique
    FunctionDynamicAssym = []
    conditionfillpositive = []
    conditionfillnegative = []
    rangexdt = max(DataFrameVerticalGrf['yRight']) - min(DataFrameVerticalGrf['yRight'])
    rangexgt = max(DataFrameVerticalGrf['yLeft']) - min(DataFrameVerticalGrf['yLeft'])

    for grf in range(0, DataFrameVerticalGrf.shape[0]):
        #FunctionDynamicAssym.append(2*(DataFrameVerticalGrf['yRight'][grf] - DataFrameVerticalGrf['yLeft'][grf])/(rangexdt+rangexgt)) # facteur 100 doit être enlevé
        FunctionDynamicAssym.append(2*(DataFrameVerticalGrf['yRight'][grf] - DataFrameVerticalGrf['yLeft'][grf])/(rangexdt+rangexgt) * 100)
        conditionfillpositive.append(FunctionDynamicAssym[grf] >= DataFrameVerticalGrf['ThresfoldPositive'][grf])
        conditionfillnegative.append(FunctionDynamicAssym[grf] <= DataFrameVerticalGrf['ThresfoldNegative'][grf])
    
    # Ajout de la FunctionDynamicAssym et des conditions fill au DataFrame
    DataFrameVerticalGrf['FunctionDynamicAssym'] = FunctionDynamicAssym
    DataFrameVerticalGrf['conditionfillpositive'] = conditionfillpositive
    DataFrameVerticalGrf['conditionfillnegative'] = conditionfillnegative

    # Procédure Graphique
    plt.figure(figsize=(15,8))
    plt.plot(DataFrameVerticalGrf['yLeft'], c='red', ls='--', label='Jambe gauche')
    plt.plot(DataFrameVerticalGrf['yRight'], c='blue', ls='--', label='Jambe droite')
    plt.plot(DataFrameVerticalGrf['FunctionDynamicAssym'], c='black', label = 'Fonction de Symétrie Dynamique')
    plt.hlines(y = Thresfold , xmin=0, xmax = DataFrameVerticalGrf.shape[0], colors='black',
                lw=0.5, ls='--', label = f'5% Thresfold (={Thresfold})')
    plt.hlines(y = -Thresfold, xmin=0, xmax = DataFrameVerticalGrf.shape[0], colors='black',
                lw=0.5, ls='--', label = f'-5% Thresfold (={-Thresfold})')
    plt.fill_between(x = range(0,DataFrameVerticalGrf.shape[0]), y1 = Thresfold, y2 = DataFrameVerticalGrf['FunctionDynamicAssym'], where = conditionfillpositive, alpha = 0.2, color = 'r')
    plt.fill_between(x = range(0,DataFrameVerticalGrf.shape[0]), y1 = -Thresfold, y2 = DataFrameVerticalGrf['FunctionDynamicAssym'], where = conditionfillnegative, alpha = 0.2, color = 'r') 
    plt.legend()
    plt.show()


def PlotDynamicSymetryFunctionNormalised(VerticalGrfRight, VerticalGrfLeft):
    # Fonction d'interpolation pour mettre sur 100 point une force de réaction au sol
    def InterpolationGrf(VerticalGrf):
        x = np.linspace(0,len(VerticalGrf),len(VerticalGrf))
        y = VerticalGrf
        f = interpolate.interp1d(x, y)
        xnew = np.linspace(0, len(VerticalGrf), 101)
        ynew = f(xnew)
        return xnew, ynew

    xnewVerticalGrfLeft, ynewVerticalGrfLeft = InterpolationGrf(VerticalGrfLeft)
    xnewVerticalGrfRight, ynewVerticalGrfRight = InterpolationGrf(VerticalGrfRight)
    
    Thresfold = 5 / 100

    DataFrameVerticalGrfLeft = pd.DataFrame({'xLeft':xnewVerticalGrfLeft,'yLeft':ynewVerticalGrfLeft})
    DataFrameVerticalGrfRight = pd.DataFrame({'xRight':xnewVerticalGrfRight,'yRight':ynewVerticalGrfRight})
    
    #return DataFrameVerticalGrfLeft, DataFrameVerticalGrfRight

    LenMaxGrf = max([DataFrameVerticalGrfRight.shape[0], DataFrameVerticalGrfLeft.shape[0]])

    ThresfoldPositive = [Thresfold] * LenMaxGrf
    ThresfoldNegative = [-Thresfold] * LenMaxGrf

    xgt = DataFrameVerticalGrfLeft['yLeft']
    xdt = DataFrameVerticalGrfRight['yRight']
    VerticalGrfAsym = []
    conditionfillpositive = []
    conditionfillnegative = []
    rangexdt = max(xdt) - min(xdt)
    rangexgt = max(xgt) - min(xgt)
    for i in range(0, LenMaxGrf):
        VerticalGrfAsym.append(2*(xdt[i]-xgt[i])/(rangexdt+rangexgt) * 100)
        #VerticalGrfAsym.append(2*(xdt[i]-xgt[i])/(rangexdt+rangexgt)) # Fateur 100 doit être enlevé
        conditionfillpositive.append(VerticalGrfAsym[i] >= ThresfoldPositive[i])
        conditionfillnegative.append(VerticalGrfAsym[i] <= ThresfoldNegative[i])

    plt.figure(figsize=(15,8))
    plt.plot(DataFrameVerticalGrfRight['yRight'], c='blue', ls='--', label='Jambe droite')
    plt.plot(DataFrameVerticalGrfLeft['yLeft'], c='r', ls='--', label='Jambe gauche')
    plt.plot(VerticalGrfAsym, c='black', label = 'Fonction de Symétrie Dynamique')

    plt.hlines(y = Thresfold, xmin=0, xmax = 100, colors='black',
                lw=0.5, ls='--', label = f'5% Thresfold (={Thresfold})')
    plt.hlines(y = -Thresfold, xmin=0, xmax = 100, colors='black',
                lw=0.5, ls='--', label = f'-5% Thresfold (={-Thresfold})')
    plt.fill_between(x = range(0, 101), y1 = ThresfoldPositive, y2 = VerticalGrfAsym, where = conditionfillpositive, alpha = 0.2, color = 'r')
    plt.fill_between(x = range(0, 101), y1 = ThresfoldNegative, y2 = VerticalGrfAsym, where = conditionfillnegative, alpha = 0.2, color = 'r')
    plt.legend()
    plt.show()