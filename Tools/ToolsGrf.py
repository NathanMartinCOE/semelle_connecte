# coding utf-8
# Author : Nathan Martin 
# Create : 2023 - 05 - 10

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
            try :     
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
            except :
                FirtPeakIndex = "NaN"
                SecondPeakIndex = "NaN"

            try :
                 MidstanceValleyIndex = argrelextrema(TabVGrf[FirtPeakIndex : SecondPeakIndex], np.less)[0][0] + FirtPeakIndex
            except :
                 MidstanceValleyIndex = "NaN"

            #Peak
            if FirtPeakIndex != "NaN":
                FirtPeak = VerticalGrf[FirtPeakIndex]
            else :
                FirtPeak = np.nan

            if MidstanceValleyIndex != "NaN":
                MidstanceValley = VerticalGrf[MidstanceValleyIndex]
            else :
                MidstanceValley = np.nan
            if SecondPeakIndex != "NaN":
                SecondPeak = VerticalGrf[SecondPeakIndex]
            else :
                SecondPeak = np.nan          
            

            # Time to.
            # Impulse.
            if FirtPeakIndex != "NaN":
                FirtPeakTimeTo = len(VerticalGrf[ :FirtPeakIndex])/FrameRate
            else :
                FirtPeakTimeTo = np.nan

            if MidstanceValleyIndex != "NaN":
                MidstanceValleyTimeTo = len(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
                TimeFromMidstanceValleyToToeOff = len(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
                FirtAndMidstanceImpulse = np.trapz(VerticalGrf[ :MidstanceValleyIndex])/FrameRate
                SecondAndPreswingImpulse = np.trapz(VerticalGrf[MidstanceValleyIndex: ])/FrameRate
            else :
                MidstanceValleyTimeTo = np.nan
                TimeFromMidstanceValleyToToeOff = np.nan
                FirtAndMidstanceImpulse = np.nan
                SecondAndPreswingImpulse = np.nan
            if SecondPeakIndex != "NaN":
                SecondPeakTimeTo = len(VerticalGrf[ :SecondPeakIndex])/FrameRate
            else :
                SecondPeakTimeTo = np.nan  

            try :
                TotalVerticalGrfImpulse = np.trapz(VerticalGrf)/FrameRate
            except :
                TotalVerticalGrfImpulse = np.nan

            """
            ----------- ANTEROPOSTERIOR GRFS -----------
            """

            #Index
            try :
                ApGrfIndexBrakingPeak = ApGrf.index(min(ApGrf))
            except: 
                ApGrfIndexBrakingPeak = "NaN"
            try :
                ApGrfIndexPropulsivePeak = ApGrf.index(max(ApGrf))
            except :
                ApGrfIndexPropulsivePeak = "NaN"
            try :
                ApGrfPower = [grf ** 2 for grf in ApGrf[ApGrfIndexBrakingPeak : ApGrfIndexPropulsivePeak]]
                ApGrfIndexZero = ApGrfIndexBrakingPeak + ApGrfPower.index(min(ApGrfPower))
            except :
                ApGrfIndexZero = "NaN"

            #Peak 
            try :
                BrakingPeak = min(ApGrf)
            except: 
                BrakingPeak = np.nan
            try :
                PropulsivePeak = max(ApGrf)
            except :
                PropulsivePeak = np.nan

            #Duration
            if ApGrfIndexZero != "NaN":
                BrakePhaseDuration = len(ApGrf[ :ApGrfIndexZero])/FrameRate
                PropulsivePhaseDuration = len(ApGrf[ApGrfIndexZero: ])/FrameRate
            else :
                BrakePhaseDuration = np.nan
                PropulsivePhaseDuration = np.nan        
            
            #Time to ..
            if ApGrfIndexBrakingPeak != "NaN":
                BrakePhaseTimeTo = len(ApGrf[ :ApGrfIndexBrakingPeak])/FrameRate
            else :
                BrakePhaseTimeTo = "NaN"
            if ApGrfIndexZero != "NaN" and ApGrfIndexPropulsivePeak != "NaN":
                PropulsivePhaseTimeTo = len(ApGrf[ApGrfIndexZero:ApGrfIndexPropulsivePeak])/FrameRate
            else :
                PropulsivePhaseTimeTo = np.nan

            #Impulse
            try :
                BrakingImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue < 0])/FrameRate
            except :
                BrakingImpulse = np.nan
            try :
                PropulsiveImpulse = np.trapz([GrfValue for GrfValue in ApGrf if GrfValue > 0])/FrameRate
            except :
                PropulsiveImpulse = np.nan

            return FirtPeak, MidstanceValley, SecondPeak, FirtPeakTimeTo, MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff, FirtAndMidstanceImpulse, SecondAndPreswingImpulse, TotalVerticalGrfImpulse, BrakingPeak, PropulsivePeak, BrakePhaseDuration, PropulsivePhaseDuration, BrakePhaseTimeTo, PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse 
