# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 03 - 01
# Modified : 2023 - 04 - 04

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dataclasses import dataclass
from matplotlib import animation
from scipy.interpolate import interp1d
from scipy.signal import argrelextrema


class AbstractWalkingKinematicsProcedure(object):
    """abstract procedure """
    def __init__(self):
        pass
    def run(self):
        pass


class GroundReactionForceKinematicsProcedure(AbstractWalkingKinematicsProcedure):
    """ Computation of the ground reaction force kinematics according Vaverka's article :
    System of gait analysis based on ground reaction force assessment.
    Acta Gymnica. 31 déc 2015;45(4):187-93. 

    This function make one dictionnary of the values of the ground reaction force in vertical axes and
    anteroposterior axes avec chaque pas en index.

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance  

    Outputs:
        GroundReactionForces a dictionnary of the values for each legs of vertical and anteroposterior 
        ground reaction force of each step. 

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

    def __init__(self):
        super(GroundReactionForceKinematicsProcedure, self).__init__()

    def run(self, walking):
        # from semelle_connecte.Tools.ToolsMakeDictStep import MakeDictStep
        from Tools.ToolsMakeDictStep import MakeDictStep
        from Tools.ToolsGrf import grf

        GroundReactionForces = dict()
        StepGrfValue = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            GrfStep = MakeDictStep(VerticalGrf = walking.m_sole[leg].data["VerticalGrf"],
                                    ApGrf = walking.m_sole[leg].data["ApGrf"],
                                    MedioLatGrf = walking.m_sole[leg].data["MediolateralGrf"])
            
            VerticalGrfStep = GrfStep["VerticalGrfStep"]
            ApGrfStep = GrfStep["ApGrfStep"]
            MedioLatGrfStep = GrfStep["MedioLatGrfStep"]

            GrfValues = {i : grf(VerticalGrfStep[i],ApGrfStep[i], FrameRate = 10) for i in range(0, len(VerticalGrfStep))}
            StepGrfValue[leg] = {"VerticalGrf" : VerticalGrfStep,
                                 "ApGrf" : ApGrfStep,
                                 "MediolateralGrf" : MedioLatGrfStep}
            GroundReactionForces[leg] = GrfValues

        walking.setStepGrfValue(StepGrfValue)
        walking.setGroundReactionForces(GroundReactionForces)



class DynamicSymetryFunctionComputeProcedure(AbstractWalkingKinematicsProcedure):
    """
    This function compute the dynamic symetry function for all value in walking.m_GroundReactionForces

    Args:
        walking.m_GroundReactionForces get by (semelle_connecte.Walking.WalkingKinematicsProcedure.GroundReactionForceKinematicsProcedure)


    Outputs:
        DataFrameDynamicSymetryScore a DataFrame of the Dynamic Symetry Function for each values of vertical and anteroposterior 
        ground reaction force of each step.

    Dynamic Symetry of :
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

    def __init__(self):
        super(DynamicSymetryFunctionComputeProcedure, self).__init__()

    def run(self, walking):

        if len(walking.m_GroundReactionForces) == 0:
            print("!!! Caution : No Ground Reaction Forces in walking object, please run the GroundReactionForceKinematicsProcedure !!!")
        else :
            DataFrameGrfValueLeft = pd.DataFrame(walking.m_GroundReactionForces["LeftLeg"]).T
            DataFrameGrfValueRight = pd.DataFrame(walking.m_GroundReactionForces["RightLeg"]).T
            Nb_ligne_min = min([DataFrameGrfValueLeft.shape[0], DataFrameGrfValueRight.shape[0]])
            DataFrameDynamicSymetryScore = pd.DataFrame(np.zeros((Nb_ligne_min, 18)))

            def FSD(ligne, col):
                xdt = DataFrameGrfValueRight.iloc[ligne,col]
                xgt = DataFrameGrfValueLeft.iloc[ligne,col]
                if max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) == 0 :
                        rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) + 1
                elif max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col]) != 0 :
                        rangexdt = max(DataFrameGrfValueRight.iloc[:,col])-min(DataFrameGrfValueRight.iloc[:,col])  
                if max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) == 0 :
                    rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) + 1
                elif max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col]) != 0 :
                    rangexgt = max(DataFrameGrfValueLeft.iloc[:,col])-min(DataFrameGrfValueLeft.iloc[:,col])
                return 2*(xdt-xgt)/(rangexdt+rangexgt)

            for ligne in range(0, Nb_ligne_min):
                for col in range(0, DataFrameGrfValueLeft.shape[1]):
                    DataFrameDynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)

            DataFrameDynamicSymetryScore = DataFrameDynamicSymetryScore.rename(columns={0:"FirtPeak", 1 : "MidstanceValley", 2 : "SecondPeak", 3 : "FirtPeakTimeTo", 
            4 : "MidstanceValleyTimeTo", 5 : "SecondPeakTimeTo", 6 : "TimeFromMidstanceValleyToToeOff", 7 : "FirtAndMidstanceImpulse", 8 :
            "SecondAndPreswingImpulse", 9 : "TotalVerticalGrfImpulse", 10 : "BrakingPeak", 11 : "PropulsivePeak", 12 : "BrakePhaseDuration", 13 :
            "PropulsivePhaseDuration", 14 : "BrakePhaseTimeTo", 15 : "PropulsivePhaseTimeTo", 16 : "BrakingImpulse", 17 : "PropulsiveImpulse"})

            walking.setDataFrameDynamicSymetryScore(DataFrameDynamicSymetryScore)

        
        def DynamicSymetryFunction(GrfRight, GrfLeft):
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

            return DataFrameGrf['FunctionDynamicAssym']

        from Tools.ToolsGetStepEvent import GetStepEvent
        HeelStrike, ToeOff = GetStepEvent(walking.m_sole["LeftLeg"].data["VerticalGrf"])

        axis = ["VerticalGrf", "ApGrf", "MediolateralGrf"] # MakeDictStep ne prend pas ML
        DictFunctionDynamicAssym = dict()

        if len(walking.m_StepGrfValue["RightLeg"]["VerticalGrf"][0]) != len(walking.m_StepGrfValue["LeftLeg"]["VerticalGrf"][0]):
            from Walking.WalkingFilters import WalkingDataProcessingFilter
            from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
            procedure = NormalisationProcedure()
            WalkingDataProcessingFilter(walking, procedure).run()

        if len(HeelStrike) == 1 :
            for axe in axis :
                if walking.m_sole["LeftLeg"].data[axe].dtype != object and walking.m_sole["RightLeg"].data[axe].dtype != object :
                    FunctionDynamicAssym = DynamicSymetryFunction(GrfRight = walking.m_StepGrfValue["RightLeg"][axe][0],
                                                GrfLeft = walking.m_StepGrfValue["LeftLeg"][axe][0])
                else :
                    print(f"No value for {axe} Ground Reaction Force")

                DictFunctionDynamicAssym[axe] = FunctionDynamicAssym

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

                    FunctionDynamicAssym = DynamicSymetryFunction(GrfRight = MeanRight["Mean"],
                                                GrfLeft = MeanLeft["Mean"])
                else :
                    print(f"No value for {axe} Ground Reaction Force")
                
                DictFunctionDynamicAssym[axe] = FunctionDynamicAssym
        
        walking.setFunctionDynamicAssym(DictFunctionDynamicAssym)


class TwoStepProcedure(AbstractWalkingKinematicsProcedure):
    """
    This function make two DataFrame with total of ground reaction force (Left + Right).

    Args:
        Walking (semelle_connecte.Walking.Walking): a walking patient instance 

    Outputs:
        LeftRight_df = a DataFrame of the sum of ground reaction force for each Left and Right step
        RightLeft_df = a DataFrame of the sum of ground reaction force for each Right and Left step     
    """

    def __init__(self):
        super(TwoStepProcedure, self).__init__()

    def run(self, walking):
        from Tools.ToolsGetStepEvent import GetStepEvent
        from Tools.ToolsInterpolationGrf import Interpolation

        Left = walking.m_sole["LeftLeg"].data["VerticalGrf"]
        Right = walking.m_sole["RightLeg"].data["VerticalGrf"]
        Sum = walking.m_sole["LeftLeg"].data["VerticalGrf"] + walking.m_sole["RightLeg"].data["VerticalGrf"]

        HeelStrikeLeft, ToeOffLeft = GetStepEvent(Left)
        HeelStrikeRight, ToeOffRight = GetStepEvent(Right)

        # firts_step = "right"
        firts_step = "left"
        LeftRight = []
        RightLeft = []

        if len(HeelStrikeLeft) == len(HeelStrikeRight):
            LenHeelStrike = len(HeelStrikeLeft)
        elif len(HeelStrikeLeft) != len(HeelStrikeRight):
            print(f"Caution : Not the same number of Heel Strike --> Left = {len(HeelStrikeLeft)} Right = {len(HeelStrikeRight)}")
            LenHeelStrike = min([len(HeelStrikeLeft), len(HeelStrikeRight)])

        if len(ToeOffLeft) == len(ToeOffRight):
            LenToeOff = len(ToeOffLeft)
        elif len(ToeOffLeft) != len(ToeOffRight):
            print(f"Caution : Not the same number of Toe Off --> Left = {len(ToeOffLeft)} Right = {len(ToeOffRight)}")  
            LenToeOff = min([len(ToeOffLeft),len(ToeOffRight)])

        if LenHeelStrike != LenToeOff:
            print("Caution : the number of HeelStrike and ToeOff are not the same !")
            LenStep = min([LenHeelStrike, LenToeOff])
        elif LenHeelStrike == LenToeOff:
            LenStep = LenHeelStrike

        for i, j in zip(np.arange(LenStep),np.arange(LenStep-1)):
            if firts_step == "right":
                RightLeft.append(Sum[HeelStrikeRight[i] : ToeOffLeft[i]])  
                LeftRight.append(Sum[HeelStrikeLeft[j] : ToeOffRight[j+1]])
            if firts_step == "left": 
                LeftRight.append(Sum[HeelStrikeLeft[i] : ToeOffRight[i]]) 
                RightLeft.append(Sum[HeelStrikeRight[j] : ToeOffLeft[j+1]])   

        LenStepLeftRight = []
        LenStepRightLeft = []
        for StepLeftRight, StepRightLeft in zip(LeftRight, RightLeft):
            LenStepLeftRight.append(len(StepLeftRight))
            LenStepRightLeft.append(len(StepRightLeft))

        LenMin = min([min(LenStepLeftRight), min(LenStepRightLeft)])

        LeftRight_df = pd.DataFrame()
        RightLeft_df = pd.DataFrame()
        i = 0
        for StepLeftRight, StepRightLeft in zip(LeftRight, RightLeft):
            xLR, yLR = Interpolation(StepLeftRight, LenMin)
            LeftRight_df[f"Step{i}"] = yLR
            xRL, yRL = Interpolation(StepRightLeft, LenMin)
            RightLeft_df[f"Step{i}"] = yRL
            i += 1

        LeftRight_df["Mean"] = LeftRight_df.mean(axis=1)
        RightLeft_df["Mean"] = RightLeft_df.mean(axis=1)
        LeftRight_df["Std"] = LeftRight_df.std(axis=1)
        RightLeft_df["Std"] = RightLeft_df.std(axis=1)
        LeftRight_df["Mean + Std"] = LeftRight_df["Mean"] + LeftRight_df["Std"]
        RightLeft_df["Mean + Std"] = RightLeft_df["Mean"] + RightLeft_df["Std"]
        LeftRight_df["Mean - Std"] = LeftRight_df["Mean"] - LeftRight_df["Std"]
        RightLeft_df["Mean - Std"] = RightLeft_df["Mean"] - RightLeft_df["Std"]

        walking.setDataFrameLeftRight(LeftRight_df)
        walking.setDataFrameRightLeft(RightLeft_df)



