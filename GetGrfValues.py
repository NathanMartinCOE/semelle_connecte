# GetGrfValues
# Author : Nathan Martin 2023 - 03 - 01

from GroundReactionForceProcedure import grf
from MakeDictStep import MakeDictStep

def GetGrfValues(VerticalGrf, ApGrf, FrameRate = 10):
    """
    This function make one dictionnary of the values of the ground reaction force in vertical axes and
    anteroposterior axes avec chaque pas en index.

    Inputs: support phase vertical ground reaction force, support phase
        anteroposterior ground reaction force

    Outputs: Dictionnary of the values of vertical and anteroposterior ground reaction force of each step
    with values order as the "grf" function (FirtPeak, MidstanceValley, SecondPeak,FirtPeakTimeTo, 
    MidstanceValleyTimeTo, SecondPeakTimeTo, TimeFromMidstanceValleyToToeOff, FirtAndMidstanceImpulse, 
    SecondAndPreswingImpulse, TotalVerticalGrfImpulse, BrakingPeak, PropulsivePeak, BrakePhaseDuration,
    PropulsivePhaseDuration, BrakePhaseTimeTo, PropulsivePhaseTimeTo, BrakingImpulse, PropulsiveImpulse)
    """
    
    VerticalGrfStep, ApGrfStep = MakeDictStep(VerticalGrf, ApGrf)
    GrfValues = {i : grf(VerticalGrfStep[i],ApGrfStep[i], FrameRate) for i in range(0, len(VerticalGrfStep))}

    return GrfValues