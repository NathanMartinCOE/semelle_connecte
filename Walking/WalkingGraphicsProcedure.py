# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 01
# Modified 2023.04.03

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import nan

from Tools.ToolsInterpolationGrf import InterpolationGrf


class AbstractWalkingGraphicsProcedure(object):
    """abstract procedure """
    def __init__(self):
        pass
    def run(self):
        pass


class PlotDynamicSymetryFunctionRealtimeProcedure(AbstractWalkingGraphicsProcedure):
    """
    This procedure create 3 plot of the dynamic symetry function of the mean ground reaction force 
    during one step in real time.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        plot of dynamic symetry function for Vertical Ground Reaction Force
        plot of dynamic symetry function for Antero-posterior Ground Reaction Force
        plot of dynamic symetry function for Medio-lateral Ground Reaction Force
    """

    def __init__(self):
        super(PlotDynamicSymetryFunctionRealtimeProcedure, self).__init__()

    def run(self, walking):

        def PlotDynamicSymetryFunctionRealtime(GrfRight, GrfLeft): 

            # Rajoute des 0 après le pas le plus court en temps
            if GrfRight.shape[0] > GrfLeft.shape[0]:
                AddZero = [0] * (GrfRight.shape[0]-GrfLeft.shape[0])
                GrfLeft = np.concatenate((GrfLeft, AddZero))
            elif GrfLeft.shape[0] > GrfRight.shape[0]:
                AddZero = [0] * (GrfLeft.shape[0]-GrfRight.shape[0])
                GrfRight = np.concatenate((GrfRight, AddZero))

            # Definition d'un thresfold de 5/100 et de -5/100 pour la FSD
            Thresfold = 5/100
            ThresfoldPositive = [Thresfold] * max([GrfRight.shape[0], GrfLeft.shape[0]])
            ThresfoldNegative = [-Thresfold] * max([GrfRight.shape[0], GrfLeft.shape[0]])

            # Création d'un DataFrame contenant les forces de réactions au sol de la jambe droite et gauche
                    # et des Thresfold positif et négatif
            DataFrameGrf = pd.DataFrame({'yRight': GrfRight,
                                         'yLeft': GrfLeft,
                                         'ThresfoldPositive': ThresfoldPositive,
                                         'ThresfoldNegative' : ThresfoldNegative})
            
            # Calcul de la fonction de symetrie dynamique
            FunctionDynamicAssym = []
            conditionfillpositive = []
            conditionfillnegative = []
            rangexdt = max(DataFrameGrf['yRight']) - min(DataFrameGrf['yRight'])
            rangexgt = max(DataFrameGrf['yLeft']) - min(DataFrameGrf['yLeft'])

            for grf in range(0, DataFrameGrf.shape[0]):
                FunctionDynamicAssym.append(2*(DataFrameGrf['yRight'][grf] - DataFrameGrf['yLeft'][grf])/(rangexdt+rangexgt)) # facteur 100 doit être enlevé
                #FunctionDynamicAssym.append(2*(DataFrameVerticalGrf['yRight'][grf] - DataFrameVerticalGrf['yLeft'][grf]) / (rangexdt + rangexgt) * 100)
                conditionfillpositive.append(FunctionDynamicAssym[grf] >= DataFrameGrf['ThresfoldPositive'][grf])
                conditionfillnegative.append(FunctionDynamicAssym[grf] <= DataFrameGrf['ThresfoldNegative'][grf])
            
            # Ajout de la FunctionDynamicAssym et des conditions fill au DataFrame
            DataFrameGrf['FunctionDynamicAssym'] = FunctionDynamicAssym
            DataFrameGrf['conditionfillpositive'] = conditionfillpositive
            DataFrameGrf['conditionfillnegative'] = conditionfillnegative

            # Procédure Graphique
            plt.figure(figsize=(15,8))
            plt.plot(DataFrameGrf['yLeft'], c='red', ls='--', label='Jambe gauche')
            plt.plot(DataFrameGrf['yRight'], c='blue', ls='--', label='Jambe droite')
            plt.plot(DataFrameGrf['FunctionDynamicAssym'], c='black', label = 'Fonction de Symétrie Dynamique')
            plt.hlines(y = Thresfold , xmin=0, xmax = DataFrameGrf.shape[0], colors='black',
                        lw=0.5, ls='--', label = f'5% Thresfold (={Thresfold})')
            plt.hlines(y = -Thresfold, xmin=0, xmax = DataFrameGrf.shape[0], colors='black',
                        lw=0.5, ls='--', label = f'-5% Thresfold (={-Thresfold})')
            plt.fill_between(x = range(0,DataFrameGrf.shape[0]), y1 = Thresfold, y2 = DataFrameGrf['FunctionDynamicAssym'], where = conditionfillpositive, alpha = 0.2, color = 'r')
            plt.fill_between(x = range(0,DataFrameGrf.shape[0]), y1 = -Thresfold, y2 = DataFrameGrf['FunctionDynamicAssym'], where = conditionfillnegative, alpha = 0.2, color = 'r') 
            plt.legend()
            plt.show()

        axis = ["VerticalGrf", "ApGrf", "MediolateralGrf"]
        for axe in axis :
            if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                PlotDynamicSymetryFunctionRealtime(GrfRight = walking.m_sole["RightLeg"].data[axe],
                                                GrfLeft = walking.m_sole["LeftLeg"].data[axe])
            else :
                print(f"No value for {axe} Ground Reaction Force")


class PlotDynamicSymetryFunctionNormalisedProcedure(AbstractWalkingGraphicsProcedure):
    """
    This procedure create 3 plot of dynamic symetry function of the mean ground reaction force 
    during one step normalised by % of step cycle.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        plot of dynamic symetry function for Vertical Ground Reaction Force
        plot of dynamic symetry function for Antero-posterior Ground Reaction Force
        plot of dynamic symetry function for Medio-lateral Ground Reaction Force
    """

    def __init__(self):
        super(PlotDynamicSymetryFunctionNormalisedProcedure, self).__init__()

    def run(self, walking):

        def PlotDynamicSymetryFunctionNormalised(GrfRight, GrfLeft):
            xnewGrfLeft, ynewGrfLeft = InterpolationGrf(GrfLeft)
            xnewGrfRight, ynewGrfRight = InterpolationGrf(GrfRight)
            
            Thresfold = 5 / 100

            DataFrameGrfLeft = pd.DataFrame({'xLeft':xnewGrfLeft,'yLeft':ynewGrfLeft})
            DataFrameGrfRight = pd.DataFrame({'xRight':xnewGrfRight,'yRight':ynewGrfRight})

            LenMaxGrf = max([DataFrameGrfRight.shape[0], DataFrameGrfLeft.shape[0]])

            ThresfoldPositive = [Thresfold] * LenMaxGrf
            ThresfoldNegative = [-Thresfold] * LenMaxGrf

            xgt = DataFrameGrfLeft['yLeft']
            xdt = DataFrameGrfRight['yRight']
            GrfAsym = []
            conditionfillpositive = []
            conditionfillnegative = []
            rangexdt = max(xdt) - min(xdt)
            rangexgt = max(xgt) - min(xgt)
            for i in range(0, LenMaxGrf):
                #GrfAsym.append(2*(xdt[i]-xgt[i])/(rangexdt+rangexgt) * 100)
                GrfAsym.append(2*(xdt[i]-xgt[i])/(rangexdt+rangexgt)) # Fateur 100 doit être enlevé
                conditionfillpositive.append(GrfAsym[i] >= ThresfoldPositive[i])
                conditionfillnegative.append(GrfAsym[i] <= ThresfoldNegative[i])

            plt.figure(figsize=(15,8))
            plt.plot(DataFrameGrfRight['yRight'], c='blue', ls='--', label='Jambe droite')
            plt.plot(DataFrameGrfLeft['yLeft'], c='r', ls='--', label='Jambe gauche')
            plt.plot(GrfAsym, c='black', label = 'Fonction de Symétrie Dynamique')

            plt.hlines(y = Thresfold, xmin=0, xmax = 100, colors='black',
                        lw=0.5, ls='--', label = f'5% Thresfold (={Thresfold})')
            plt.hlines(y = -Thresfold, xmin=0, xmax = 100, colors='black',
                        lw=0.5, ls='--', label = f'-5% Thresfold (={-Thresfold})')
            plt.fill_between(x = range(0, 100), y1 = ThresfoldPositive, y2 = GrfAsym, where = conditionfillpositive, alpha = 0.2, color = 'r')
            plt.fill_between(x = range(0, 100), y1 = ThresfoldNegative, y2 = GrfAsym, where = conditionfillnegative, alpha = 0.2, color = 'r')
            plt.legend()
            plt.show()

        axis = ["VerticalGrf", "ApGrf", "MediolateralGrf"]
        for axe in axis :
            if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                PlotDynamicSymetryFunctionNormalised(GrfRight = walking.m_sole["RightLeg"].data[axe],
                                                GrfLeft = walking.m_sole["LeftLeg"].data[axe])
            else :
                print(f"No value for {axe} Ground Reaction Force")


class PlotCutGroundReactionForceProcedure(AbstractWalkingGraphicsProcedure):
    """
    This procedure create 3 subplot (one for each axis) in each subplot "n" plot for the number of cut
    each graph represente the mean Ground Reaction Force for an axis.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        "n" plot with mean Vertical Ground Reaction Force
        "n" plot with mean Antero-posterior Ground Reaction Force
        "n" plot with mean Medio-lateral Ground Reaction Force
    """

    def __init__(self):
        super(PlotCutGroundReactionForceProcedure, self).__init__()

    def run(self, walking):
        # from semelle_connecte.Tools.ToolsMakeDictStep import MakeDictStep
        from Tools.ToolsMakeDictStep import MakeDictStep
        # from Tools.ToolsMakeDictStep import MakeDictStepForCut

        def MeanCutDataGrf(GrfDataframeCut):
            antGrf = [0] * GrfDataframeCut.shape[0]
            MeanCutDataGrf = pd.DataFrame()

            for colname in GrfDataframeCut.columns:
                VerticalGrfStep, ant_vide = MakeDictStep(pd.array(GrfDataframeCut[colname]), antGrf)
                ListNa0 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[0]))
                ListNa40 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[len(VerticalGrfStep) - 1]))
                VerticalGrfStep[0] = np.concatenate((ListNa0, VerticalGrfStep[0]))
                VerticalGrfStep[len(VerticalGrfStep) - 1] = np.concatenate((VerticalGrfStep[len(VerticalGrfStep) - 1], ListNa40))
                VerticalGrfStepDataFrame = pd.DataFrame()
                for i in range(0, len(VerticalGrfStep)-1):
                    VerticalGrfStepDataFrame[f"Step{i}"] = VerticalGrfStep[i]  
                MeanCutDataGrf[f"Mean{colname}"] = VerticalGrfStepDataFrame.mean(axis = 1)

            return MeanCutDataGrf
        def PlotCutDataGrf(MeanGrfDataframeCut):

            MeanGrfDataframeCutLeft = pd.DataFrame()
            MeanGrfDataframeCutRight = pd.DataFrame()
            for colIndex in zip(range(0, MeanGrfDataframeCut.shape[1], 2),
                                range(1,MeanGrfDataframeCut.shape[1] + 1, 2)):
                MeanGrfDataframeCutLeft[colIndex] = MeanGrfDataframeCut[MeanGrfDataframeCut.columns[colIndex[0]]]
                MeanGrfDataframeCutRight[colIndex] = MeanGrfDataframeCut[MeanGrfDataframeCut.columns[colIndex[1]]]
            MeanGrfDataframeCutLeft["MeanOfLeft"] = MeanGrfDataframeCutLeft.mean(axis = 1)
            MeanGrfDataframeCutRight["MeanOfRight"] = MeanGrfDataframeCutRight.mean(axis = 1)

            figIndex = 0
            plt.figure(figsize=(15,5))
            for cut in np.arange(MeanGrfDataframeCut.columns.shape[0]//2):
                plt.subplot(1, MeanGrfDataframeCut.columns.shape[0]//2, cut+1)
                plt.plot(MeanGrfDataframeCut[MeanGrfDataframeCut.columns[figIndex]], c="red", label="Left")
                plt.plot(MeanGrfDataframeCut[MeanGrfDataframeCut.columns[figIndex +1]], c="blue", label="Right")
                plt.plot(MeanGrfDataframeCutLeft["MeanOfLeft"], c="red", ls="--", label="Left Mean")
                plt.plot(MeanGrfDataframeCutRight["MeanOfRight"], c="blue", ls="--", label="Right Mean")
                figIndex += 2
            plt.legend(ncol = 4,
                    loc = "center",
                    bbox_to_anchor = (((-0.61 * ((MeanGrfDataframeCut.columns.shape[0]//2)-2)) - 0.11), -0.14))

        MeanGrfDataframeCut = MeanCutDataGrf(walking.m_DictOfDataFrameCutGrf["VerticalGrf"])
        PlotCutDataGrf(MeanGrfDataframeCut)
        
