# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 01
# Modified 2023.04.03

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import nan
import os

from Tools.ToolsInterpolationGrf import InterpolationGrf
from Walking.WalkingFilters import WalkingDataProcessingFilter, WalkingKinematicsFilter
from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure, GroundReactionForceKinematicsProcedure

class AbstractWalkingGraphicsProcedure(object):
    """abstract procedure """
    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        self.m_show_graph = show_graph
        self.m_save_graph = save_graph
        self.m_StoragePath = StoragePath

    def run(self):
        pass


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

    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        super(PlotDynamicSymetryFunctionNormalisedProcedure, self).__init__(show_graph, save_graph, StoragePath)

    def run(self, walking):

        def PlotDynamicSymetryFunction(GrfRight, GrfLeft):

            # Rajoute des 0 après le pas le plus court en temps
            if GrfRight.shape[0] > GrfLeft.shape[0]:
                AddZero = [0] * (GrfRight.shape[0]-GrfLeft.shape[0])
                GrfLeft = np.concatenate((GrfLeft, AddZero))
            elif GrfLeft.shape[0] > GrfRight.shape[0]:
                AddZero = [0] * (GrfLeft.shape[0]-GrfRight.shape[0])
                GrfRight = np.concatenate((GrfRight, AddZero))

            # Definition d'un thresfold de 5% et de -5% pour la FSD
            Thresfold = 5
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
                # FunctionDynamicAssym.append(2*(DataFrameGrf['yRight'][grf] - DataFrameGrf['yLeft'][grf])/(rangexdt+rangexgt)) # facteur 100 doit être enlevé
                FunctionDynamicAssym.append(2*(DataFrameGrf['yRight'][grf] - DataFrameGrf['yLeft'][grf]) / (rangexdt + rangexgt) * 100)
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
            if self.m_save_graph == True:
                try :
                    plt.savefig(os.path.join(self.m_StoragePath,f'Assym{axe}.png'))
                except :
                    print(f"Can't save plot to {self.m_StoragePath} { f'Assym{axe}.png'}")
            if self.m_show_graph == True:
                plt.show()


        from Tools.ToolsGetStepEvent import GetStepEvent
        HeelStrike, ToeOff = GetStepEvent(walking.m_sole["LeftLeg"].data["VerticalGrf"])

        axis = ["VerticalGrf", "ApGrf", "MediolateralGrf"] # MediolateralGrf peut entrainer des bug

        if len(HeelStrike) == 1 :
            for axe in axis :
                if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                    PlotDynamicSymetryFunction(GrfRight = walking.m_StepGrfValue["RightLeg"][axe][0],
                                               GrfLeft = walking.m_StepGrfValue["LeftLeg"][axe][0])
                else :
                    print(f"No value for {axe} Ground Reaction Force")


        elif len(HeelStrike)>1 :
            for axe in axis :
                if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                    MeanLeft = pd.DataFrame()
                    MeanRight = pd.DataFrame()

                    for step in np.arange(len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"])):
                        MeanLeft[f"Step{step}"] = walking.m_StepGrfValue["LeftLeg"][axe][step]
                    for step in np.arange(len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"])):
                        MeanRight[f"Step{step}"] = walking.m_StepGrfValue["RightLeg"][axe][step]

                    df_zero = pd.DataFrame([[0.0] * len(MeanLeft.columns)], columns= MeanLeft.columns)
                    MeanLeft = MeanLeft.append(df_zero, ignore_index=True)
                    df_zero = pd.DataFrame([[0.0] * len(MeanRight.columns)], columns= MeanRight.columns)
                    MeanRight = MeanRight.append(df_zero, ignore_index=True)

                    MeanLeft["Mean"] = MeanLeft.mean(axis=1)
                    MeanRight["Mean"] = MeanRight.mean(axis=1)

                    PlotDynamicSymetryFunction(GrfRight = MeanRight["Mean"],
                                               GrfLeft = MeanLeft["Mean"])
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

    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        super(PlotCutGroundReactionForceProcedure, self).__init__(show_graph, save_graph, StoragePath)

    def run(self, walking):
        # from semelle_connecte.Tools.ToolsMakeDictStep import MakeDictStep
        from Tools.ToolsMakeDictStep import MakeDictStep
        # from Tools.ToolsMakeDictStep import MakeDictStepForCut

        def MeanCutDataGrf(GrfDataframeCut):
            from Tools.ToolsInterpolationGrf import Interpolation
            antGrf = walking.m_sole["LeftLeg"].data["ApGrf"]
            MedioLatGrf = walking.m_sole["LeftLeg"].data["MediolateralGrf"]
            MeanCutDataGrf = pd.DataFrame()

            for colname in GrfDataframeCut.columns:
                GrfStep = MakeDictStep(pd.array(GrfDataframeCut[colname]), antGrf, MedioLatGrf)

                VerticalGrfStep = GrfStep["VerticalGrfStep"]
                ApGrfStep = GrfStep["ApGrfStep"]
                MedioLatGrfStep = GrfStep["MedioLatGrfStep"]

                ListNa0 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[0]))
                ListNa40 = [nan] * (len(VerticalGrfStep[len(VerticalGrfStep)//2]) - len(VerticalGrfStep[len(VerticalGrfStep) - 1]))
                VerticalGrfStep[0] = np.concatenate((ListNa0, VerticalGrfStep[0]))
                VerticalGrfStep[len(VerticalGrfStep) - 1] = np.concatenate((VerticalGrfStep[len(VerticalGrfStep) - 1], ListNa40))
                VerticalGrfStepDataFrame = pd.DataFrame()
                for i in range(0, len(VerticalGrfStep)-1):
                    x, VerticalGrfStepDataFrame[f"Step{i}"] = Interpolation(VerticalGrfStep[i], xnew_num= 1000)
                MeanCutDataGrf[f"Mean{colname}"] = VerticalGrfStepDataFrame.mean(axis = 1, skipna=True)

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
            if self.m_save_graph == True:
                try :
                    plt.savefig(os.path.join(self.m_StoragePath,f'CutDataGrf.png'))
                except :
                    print(f"Can't save plot to {self.m_StoragePath} CutDataGrf.png")
            if self.m_show_graph == True:
                plt.show()

        MeanGrfDataframeCut = MeanCutDataGrf(walking.m_DictOfDataFrameCutGrf["VerticalGrf"])
        PlotCutDataGrf(MeanGrfDataframeCut)

        
class PlotMaxAndMinAsymetryProcedure(AbstractWalkingGraphicsProcedure):
    """
    1) Faits un plots de l'asymétrie d'un des paramètres de ground reaction force au cours du temps 
    2) Recherche le pas ou l'asymétrie sur ce paramètre est la plus importante et le plot
    3) Recherche le pas ou l'asymétrie sur ce paramètre est la moins importante et le plot
    Args name and num :
    0 : FirtPeak                                    10 : BrakingPeak
    1 : MidstanceValley                             11 : PropulsivePeak
    2 : SecondPeak                                  12 : BrakePhaseDuration
    3 : FirtPeakTimeTo                              13 : PropulsivePhaseDuration
    4 : MidstanceValleyTimeTo                       14 : BrakePhaseTimeTo
    5 : SecondPeakTimeTo                            15 : PropulsivePhaseTimeTo
    6 : TimeFromMidstanceValleyToToeOff             16 : BrakingImpulse
    7 : FirtAndMidstanceImpulse                     17 : PropulsiveImpulse
    8 : SecondAndPreswingImpulse
    9 : TotalVerticalGrfImpulse 
    """

    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        super(PlotMaxAndMinAsymetryProcedure, self).__init__(show_graph, save_graph, StoragePath)

    def run(self, walking):

        def FindMaxAndMinAsym(walking, names, nums, axe):
            for name, num in zip(names, nums):
                listvalue = []
                for step in np.arange(len(walking.m_GroundReactionForces['LeftLeg'])):
                    listvalue.append(walking.m_GroundReactionForces['LeftLeg'][step][num])
                for step in np.arange(len(walking.m_GroundReactionForces['RightLeg'])):
                    listvalue.append(walking.m_GroundReactionForces['RightLeg'][step][num])

                thresfold5 = max([abs(val) for val in listvalue]) * 5/100
                thresfold10 = max([abs(val) for val in listvalue]) * 10/100

                try :
                    StepAsymMax = np.nanargmax(np.asarray([abs(val) ** 2 for val in walking.m_DataFrameDynamicSymetryScore[name]]))

                    print("Score d'asymétrie :")
                    print("-valeur positive = valeur jambe droite > valeur jambe gauche")
                    print("-valeur négative = valeur jambe gauche > valeur jambe droite")
                    print(f"Le pas le plus asymétrique sur le paramètre {name} est le pas numéro {StepAsymMax}")
                    plt.figure(figsize=(10,5))
                    plt.subplot(1,2,1)
                    plt.plot(walking.m_StepGrfValue["LeftLeg"][axe][StepAsymMax], c='r', label='Left')
                    plt.plot(walking.m_StepGrfValue["RightLeg"][axe][StepAsymMax], c='blue', label='Right')
                    plt.legend()
                    plt.subplot(1,2,2)
                    LenStep = len(walking.m_StepGrfValue["LeftLeg"][axe])
                    plt.scatter(x = np.arange(len(walking.m_DataFrameDynamicSymetryScore[name])),
                                y = walking.m_DataFrameDynamicSymetryScore[name])
                    plt.hlines(y= thresfold10, xmin=0, xmax=LenStep, colors='red', ls='--', label=f"10% : {round(thresfold10,2)}")
                    plt.hlines(y= thresfold5, xmin=0, xmax=LenStep, colors='black', ls='--', label=f"5% : {round(thresfold5,2)}")
                    plt.hlines(y= 0, xmin=0, xmax=LenStep, colors='black')
                    plt.hlines(y= - thresfold5, xmin=0, xmax=LenStep, colors='black', ls='--')
                    plt.hlines(y= - thresfold10, xmin=0, xmax=LenStep, colors='red', ls='--')
                    plt.scatter(x= StepAsymMax, y= walking.m_DataFrameDynamicSymetryScore[name][StepAsymMax], c='r')
                    plt.legend()
                    if self.m_save_graph == True:
                        try :
                            plt.savefig(os.path.join(self.m_StoragePath,f'{name}_MaxAssym.png'))
                        except :
                            print(f"Can't save plot to {self.m_StoragePath} {name}_MaxAssym.png'")
                    if self.m_show_graph == True:
                            plt.show()

                    StepAsymMin = np.nanargmin(np.asarray([abs(val) ** 2 for val in walking.m_DataFrameDynamicSymetryScore[name]]))

                    print(f"Le pas le moins asymétrique sur le paramètre {name} est le pas numéro {StepAsymMin}")
                    plt.figure(figsize=(10,5))
                    plt.subplot(1,2,1)
                    plt.plot(walking.m_StepGrfValue["LeftLeg"][axe][StepAsymMin], c='r', label='Left')
                    plt.plot(walking.m_StepGrfValue["RightLeg"][axe][StepAsymMin], c='blue', label='Right')
                    plt.legend()
                    plt.subplot(1,2,2)
                    LenStep = len(walking.m_StepGrfValue["LeftLeg"][axe])
                    plt.scatter(x = np.arange(len(walking.m_DataFrameDynamicSymetryScore[name])),
                                y = walking.m_DataFrameDynamicSymetryScore[name])
                    plt.hlines(y= thresfold10, xmin=0, xmax=LenStep, colors='red', ls='--', label=f"10% : {round(thresfold10,2)}")
                    plt.hlines(y= thresfold5, xmin=0, xmax=LenStep, colors='black', ls='--', label=f"5% : {round(thresfold5,2)}")
                    plt.hlines(y= 0, xmin=0, xmax=LenStep, colors='black')
                    plt.hlines(y= - thresfold5, xmin=0, xmax=LenStep, colors='black', ls='--')
                    plt.hlines(y= - thresfold10, xmin=0, xmax=LenStep, colors='red', ls='--')
                    plt.scatter(x= StepAsymMin, y= walking.m_DataFrameDynamicSymetryScore[name][StepAsymMin], c='r')
                    plt.legend()
                    if self.m_save_graph == True:
                        try :
                            plt.savefig(os.path.join(self.m_StoragePath,f'{name}_MinAssym.png'))
                        except :
                            print(f"Can't save plot to {self.m_StoragePath} {name}_MinAssym.png'")
                    if self.m_show_graph == True:
                            plt.show()

                except :
                    print(f" ================================ All value for {name} = NaN ================================")

        names = ["FirtPeak", "MidstanceValley", "SecondPeak", "FirtPeakTimeTo", "MidstanceValleyTimeTo", "SecondPeakTimeTo", "TimeFromMidstanceValleyToToeOff", "FirtAndMidstanceImpulse", "SecondAndPreswingImpulse", "TotalVerticalGrfImpulse"]
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        FindMaxAndMinAsym(walking, names, nums, axe="VerticalGrf")

        names = ["BrakingPeak", "PropulsivePeak", "BrakePhaseDuration", "PropulsivePhaseDuration", "BrakePhaseTimeTo", "PropulsivePhaseTimeTo", "BrakingImpulse", "PropulsiveImpulse"]
        nums = [10, 11, 12, 13, 14, 15, 16, 17]
        FindMaxAndMinAsym(walking, names, nums, axe="ApGrf")


class PlotWorthAndBestStepProcedure(AbstractWalkingGraphicsProcedure):
    """
    This procedure find the step witch maximize or minimazie the asymetry for all parameter.
    
    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  
    
    Outputs :
        Return 6 plots :
            - Maximal asymetry for all parameter (the worth step)
            - Maximal asymetry for Vertical Grf parameter (the worth step in Vertical Grf)
            - Maximal asymetry for AntPost Grf parameter (the worth step in AntPost Grf)
            - Minimal asymetry for all parameter (the best step)
            - Minimal asymetry for Vertical Grf parameter (the best step in Vertical Grf)
            - Minimal asymetry for AntPost Grf parameter (the best step in AntPost Grf)
    """

    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        super(PlotWorthAndBestStepProcedure, self).__init__(show_graph, save_graph, StoragePath)

    def run(self, walking):
        if len(walking.m_DataFrameDynamicSymetryScore)==0:
            procedure = NormalisationProcedure()
            WalkingDataProcessingFilter(walking, procedure).run()
            procedure = GroundReactionForceKinematicsProcedure()
            WalkingKinematicsFilter(walking, procedure).run()
            procedure = DynamicSymetryFunctionComputeProcedure()
            WalkingKinematicsFilter(walking, procedure).run()

        data = walking.m_DataFrameDynamicSymetryScore
        data = abs(data)
        data["SumAsymTotal"] = data.sum(axis=1)
        data["SumAsymVertical"] = data[["FirtPeak", "MidstanceValley", "SecondPeak", "FirtPeakTimeTo", "MidstanceValleyTimeTo", "SecondPeakTimeTo", "TimeFromMidstanceValleyToToeOff", "FirtAndMidstanceImpulse", "SecondAndPreswingImpulse", "TotalVerticalGrfImpulse"]][:].sum(axis=1)
        data["SumAsymAntpost"] = data[["BrakingPeak", "PropulsivePeak", "BrakePhaseDuration", "PropulsivePhaseDuration", "BrakePhaseTimeTo", "PropulsivePhaseTimeTo", "BrakingImpulse", "PropulsiveImpulse"]][:].sum(axis=1)

        steps = []
        steps.append(data["SumAsymTotal"].argmax())
        steps.append(data["SumAsymVertical"].argmax())
        steps.append(data["SumAsymAntpost"].argmax())
        steps.append(data["SumAsymTotal"].argmin())
        steps.append(data["SumAsymVertical"].argmin())
        steps.append(data["SumAsymAntpost"].argmin())
        
        titles = ["Step with maximal asymetry in Vertical and AntPost Grf", "Step with maximal asymetry in Vertical Grf", "Step with maximal asymetry in AntPost Grf", "Step with minimal asymetry in Vertical and AntPost Grf", "Step with minimal asymetry in Vertical Grf", "Step with minimal asymetry in AntPost Grf"]

        for step, title in zip(steps, titles):
            plt.figure(figsize=(10,5))
            plt.subplot(1,2,1)
            plt.title(title)
            plt.plot(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][step], c='r', label='Left')
            plt.plot(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][step], c='blue', label='Right')
            plt.subplot(1,2,2)
            plt.plot(walking.m_StepGrfValue["LeftLeg"]["ApGrf"][step], c='r', label='Left')
            plt.plot(walking.m_StepGrfValue["RightLeg"]["ApGrf"][step], c='blue', label='Right')
            if self.m_save_graph == True:
                try :
                    plt.savefig(os.path.join(self.m_StoragePath,f'{title}.png'))
                except :
                    print(f"Can't save plot to {self.m_StoragePath} {title}.png'")
            if self.m_show_graph == True:
                    plt.show()

class PlotTwoStepProcedure(AbstractWalkingGraphicsProcedure):
    """
    This procedure plot the sum of vertical ground reaction force for right-left and left-right steps.
    
    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  
    
    Outputs :
        Return 3 plots :
            - Sum of vertical ground reaction force of mean Left-Right step and mean Right-Left step
            - Sum of vertical ground reaction force of mean Left-Right step +- std
            - Sum of vertical ground reaction force of mean Right-Left step +- std
    """

    def __init__(self, show_graph = True, save_graph = False, StoragePath = None):
        super(PlotTwoStepProcedure, self).__init__(show_graph , save_graph, StoragePath)

    def run(self, walking):
        DataFrameLeftRight = walking.m_DataFrameLeftRight
        DataFrameRightLeft= walking.m_DataFrameRightLeft

        plt.figure(figsize=(10,10))
        plt.subplot(3,1,1)
        plt.title("Left Right and Right Left")
        plt.plot(DataFrameLeftRight["Mean"], c="r", label="Left Right")
        plt.plot(DataFrameRightLeft["Mean"], c="b",  label="Right Left")
        plt.xticks([])
        plt.legend()
        plt.subplot(3,1,2)
        plt.title("Left Right")
        plt.plot(DataFrameLeftRight["Mean"], c="black")
        plt.plot(DataFrameLeftRight["Mean + Std"], c="grey")
        plt.plot(DataFrameLeftRight["Mean - Std"], c="grey")
        plt.xticks([])
        plt.subplot(3,1,3)
        plt.title("Right Left")
        plt.plot(DataFrameRightLeft["Mean"], c="black")
        plt.plot(DataFrameRightLeft["Mean + Std"], c="grey")
        plt.plot(DataFrameRightLeft["Mean - Std"], c="grey")
        plt.xticks([])
        if self.m_save_graph == True:
            try :
                plt.savefig(os.path.join(self.m_StoragePath,'TwoStep.png'))
            except :
                print(f"Can't save plot to {self.m_StoragePath} TwoStep.png'")
        if self.m_show_graph == True:
                plt.show()