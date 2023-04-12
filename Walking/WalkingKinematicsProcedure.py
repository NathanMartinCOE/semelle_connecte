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
            if argrelextrema(TabVGrf, np.greater)[0].shape[0] > 2:
                LocalMaxDataFrame = pd.DataFrame()
                LocalMaxDataFrame["ListIndexMax"] = list(argrelextrema(TabVGrf, np.greater)[0])
                LocalMaxDataFrame["ListValueMax"] = [VerticalGrf[index] for index in LocalMaxDataFrame["ListIndexMax"]]
                LocalMaxDataFrame = LocalMaxDataFrame.sort_values(by="ListValueMax", ascending=False)
                index0, index1 = LocalMaxDataFrame["ListIndexMax"][0:2].values
                if index0 < index1 :
                    FirtPeakIndex = index0
                    SecondPeakIndex = index1
                elif index0 > index1 :
                    FirtPeakIndex = index1
                    SecondPeakIndex = index0
            else :
                FirtPeakIndex = argrelextrema(TabVGrf, np.greater)[0][0]
                SecondPeakIndex = argrelextrema(TabVGrf, np.greater)[0][1]
            MidstanceValleyIndex = argrelextrema(TabVGrf[FirtPeakIndex : SecondPeakIndex], np.less)[0][0] + FirtPeakIndex

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
        
            """
            This function make two dictionnary of the ground reaction force in vertical axes and
            anteroposterior axes with each step in index. Use a rolling median with a step size of 30 
            to smooth out data loss.

            Inputs: support phase vertical ground reaction force, support phase
                anteroposterior ground reaction force

            Outputs: Dictionnary of the vertical ground reaction force of each step, 
            Dictionnary of the anteroposterior ground reaction force of each step  
            """
            if min(VerticalGrf) != 0 :
                thresfold = min(VerticalGrf) + 10 / 100 * min(VerticalGrf)
                print(f"Caution no 0 find in Vertical GRF dataframe : use of a thresfold at {thresfold}")
            else : thresfold = 0

            def GetStepEvent(VerticalGrf):
                HeelStrike = []
                ToeOff = []
                for i in range(0,len(VerticalGrf)-1):
                    if thresfold == 0:
                        if VerticalGrf[i] == 0 and VerticalGrf[i+1] > 0 : 
                            HeelStrike.append(i)
                        if VerticalGrf[i] > 0 and VerticalGrf[i+1] == 0 : 
                            ToeOff.append(i)
                    else :
                        if VerticalGrf[i] < thresfold  and VerticalGrf[i+1] > thresfold : 
                            HeelStrike.append(i)
                        if VerticalGrf[i] > thresfold and VerticalGrf[i+1] < thresfold : 
                            ToeOff.append(i)
                return HeelStrike, ToeOff
            
            def RollingMedian(VerticalGrf, RollingMedianStep = 30):
                RollingMedianGrf = [abs(value) for value in VerticalGrf]
                RollingMedianGrf = pd.DataFrame(RollingMedianGrf)
                RollingMedianGrf = RollingMedianGrf.rolling(window = RollingMedianStep, center = True).median()
                RollingMedianGrf = RollingMedianGrf.fillna(0)
                RollingMedianGrf = RollingMedianGrf[0].tolist()
                return RollingMedianGrf
            
            # HeelStrike, ToeOff = GetStepEvent(RollingMedian(VerticalGrf)) # Si présence de NaN dans les data peut être utile
            HeelStrike, ToeOff = GetStepEvent(VerticalGrf)
            VerticalGrfStep = {i : VerticalGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)}
            ApGrfStep = {i : ApGrf[HeelStrike[i]:ToeOff[i]] for i in np.arange(len(HeelStrike)-1)}
            return VerticalGrfStep, ApGrfStep

        GroundReactionForces = dict()
        StepGrfValue = dict()
        for leg in ["LeftLeg", "RightLeg"]:
            VerticalGrfStep, ApGrfStep = MakeDictStep(VerticalGrf = walking.m_sole[leg].data["VerticalGrf"],
                                                      ApGrf = walking.m_sole[leg].data["ApGrf"])
            GrfValues = {i : grf(VerticalGrfStep[i],ApGrfStep[i], FrameRate = 10) for i in range(0, len(VerticalGrfStep))}
            StepGrfValue[leg] = {"VerticalGrf" : VerticalGrfStep,
                                 "ApGrf" : ApGrfStep}
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
            DataFrameDynamicSymetryScore = pd.DataFrame(np.zeros(DataFrameGrfValueLeft.shape))

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

            for ligne in range(0,DataFrameGrfValueLeft.shape[0]):
                for col in range(0,DataFrameGrfValueLeft.shape[1]):
                    DataFrameDynamicSymetryScore.iloc[ligne,col] = FSD(ligne,col)

            DataFrameDynamicSymetryScore = DataFrameDynamicSymetryScore.rename(columns={0:"FirtPeak", 1 : "MidstanceValley", 2 : "SecondPeak", 3 : "FirtPeakTimeTo", 
            4 : "MidstanceValleyTimeTo", 5 : "SecondPeakTimeTo", 6 : "TimeFromMidstanceValleyToToeOff", 7 : "FirtAndMidstanceImpulse", 8 :
            "SecondAndPreswingImpulse", 9 : "TotalVerticalGrfImpulse", 10 : "BrakingPeak", 11 : "PropulsivePeak", 12 : "BrakePhaseDuration", 13 :
            "PropulsivePhaseDuration", 14 : "BrakePhaseTimeTo", 15 : "PropulsivePhaseTimeTo", 16 : "BrakingImpulse", 17 : "PropulsiveImpulse"})

            walking.setDataFrameDynamicSymetryScore(DataFrameDynamicSymetryScore)
