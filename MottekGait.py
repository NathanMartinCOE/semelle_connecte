import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking
from Tools.ToolsFFT import TransformFourrier


DataPath = 'C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\grf\\'
Path = DataPath + 'gait_test4.c3d' 
# Path = DataPath + 'gait_test5.c3d' # fait 50 pas

acq = btkTools.smartReader(Path)
grwc = btkTools.getForcePlateWrench(acq)
mass = 60 # en kg

forces = []
items = [0,1]
for it in items:
    forces.append(grwc.GetItem(it).GetForce().GetValues() / (mass * 9.81) * 100)

dataLeft = pd.DataFrame()
dataLeft["VerticalVGrf"] = TransformFourrier(forces[1][:,2], seuil=10000) 
dataLeft["VerticalVGrf"][dataLeft["VerticalVGrf"] < 10] = 0
dataLeft["ApGrf"] = TransformFourrier(forces[1][:,1], seuil=5000)
dataLeft["MediolateralGrf"] = TransformFourrier(forces[1][:,0] * -1, seuil=1300)

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = TransformFourrier(forces[0][:,2], seuil=10000) 
dataRight["VerticalVGrf"][dataRight["VerticalVGrf"] < 10] = 0
dataRight["ApGrf"] = TransformFourrier(forces[0][:,1], seuil=5000)
dataRight["MediolateralGrf"] = TransformFourrier(forces[0][:,0], seuil=1300)


SoleInstanceLeft = FeetMe(1000)
SoleInstanceLeft.SetGroundReactionForce("Vertical", dataLeft["VerticalVGrf"].to_numpy())
SoleInstanceLeft.SetGroundReactionForce("Ap", dataLeft["ApGrf"].to_numpy())
SoleInstanceLeft.SetGroundReactionForce("Mediolateral", dataLeft["MediolateralGrf"].to_numpy())
SoleInstanceLeft.constructTimeseries()

SoleInstanceRight = FeetMe(1000)
SoleInstanceRight.SetGroundReactionForce("Vertical", dataRight["VerticalVGrf"].to_numpy())
SoleInstanceRight.SetGroundReactionForce("Ap", dataRight["ApGrf"].to_numpy())
SoleInstanceRight.SetGroundReactionForce("Mediolateral", dataRight["MediolateralGrf"].to_numpy())
SoleInstanceRight.constructTimeseries()

walking = Walking(mass)
walking.setLeftLegSole(SoleInstanceLeft)
walking.setRightLegSole(SoleInstanceRight)



from Walking.WalkingFilters import WalkingKinematicsFilter
from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
procedure = GroundReactionForceKinematicsProcedure()
WalkingKinematicsFilter(walking, procedure).run()

from Walking.WalkingFilters import WalkingDataProcessingFilter
from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
procedure = NormalisationProcedure()
WalkingDataProcessingFilter(walking, procedure).run()


from Walking.WalkingFilters import WalkingDataProcessingFilter
from Walking.WalkingDataProcessingProcedure import DeleteStepProcedure

procedure = DeleteStepProcedure()
WalkingDataProcessingFilter(walking, procedure).run()

from Walking.WalkingFilters import WalkingGraphicsFilter
from Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure

procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
WalkingGraphicsFilter(walking, procedure).run()




