# pytest -q --disable-pytest-warnings  TestForcePlate.py

# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Walking::test_Initialisation_Walking

# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Kinematics::test_GroundReactionForceKinematicsProcedure
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Kinematics::test_DynamicSymetryFunctionComputeProcedure
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Kinematics::test_TwoStepProcedure ## caution !!

# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_DataProcessing::test_NormalisationProcedure
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_DataProcessing::test_CutDataProcessingProcedure ## caution !!

# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Graphics::test_PlotMaxAndMinAsymetryProcedure ## caution !!
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Graphics::test_PlotWorthAndBestStepProcedure ## caution !!
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Graphics::test_PlotCutGroundReactionForceProcedure ## caution !!
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Graphics::test_PlotTwoStepProcedure ## caution !!
# pytest -s --disable-pytest-warnings  TestForcePlate.py::Test_Graphics::test_PlotDynamicSymetryFunctionNormalisedProcedure

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from semelle_connecte.SOLE.FeetMe import FeetMe
from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.Tools.ToolsFFT import TransformFourrier


DataPath = 'C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\grf\\'
Path = DataPath + 'test_grf01.c3d'

acq = btkTools.smartReader(Path)
grwc = btkTools.getForcePlateWrench(acq)
mass = 60 # en kg

def RollingMean(data, Step = 10):
    filtered = [value for value in data]
    filtered = pd.DataFrame(filtered)
    filtered = filtered.rolling(window = Step, center = True).mean()
    filtered = filtered.fillna(0)
    filtered = filtered[0].tolist()
    return np.array(filtered)

def SetZeroVertical(filtered):
    for index in np.arange(len(filtered)):
        if filtered[index] < 1:
            filtered[index] = 0
    return filtered

forces = dict()
plateformes = [0,1,2]

for plateforme in plateformes:
    data = grwc.GetItem(plateforme).GetForce().GetValues() / mass 
    filtered0 = RollingMean(data[:,0])
    filtered1 = RollingMean(data[:,1])
    filtered2 = SetZeroVertical(RollingMean(data[:,2]))
    forces[plateforme] = {"Ve" : np.abs(filtered2),
                          "Ap" : filtered1,
                          "Ml" : filtered0}    


dataLeft = pd.DataFrame()
dataLeft["VerticalVGrf"] = forces[1]["Ve"] #VerticalGrfLeft
dataLeft["ApGrf"] = forces[1]["Ap"]#ApGrfLeft
dataLeft["MediolateralGrf"] = forces[1]["Ml"] #MediolateralGrfLeft

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = forces[0]["Ve"] #VerticalGrfRight
dataRight["ApGrf"] = forces[0]["Ap"] #ApGrfRight
dataRight["MediolateralGrf"] = forces[0]["Ml"] #MediolateralGrfRight

class Test_Walking:

    def test_Initialisation_Walking(self):
        
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



class Test_Kinematics:

    def test_GroundReactionForceKinematicsProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure

        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

    def test_DynamicSymetryFunctionComputeProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
    
    # def test_TwoStepProcedure(self):
    #     from Walking.WalkingFilters import WalkingKinematicsFilter
    #     from Walking.WalkingKinematicsProcedure import TwoStepProcedure

    #     procedure = TwoStepProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()


class Test_DataProcessing:

    def test_NormalisationProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure

        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

    # def test_CutDataProcessingProcedure(self):

    #     from Walking.WalkingFilters import WalkingDataProcessingFilter
    #     from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

    #     procedure = CutDataProcessingProcedure()
    #     procedure.setCutNumber(n_cut=3)
    #     WalkingDataProcessingFilter(walking, procedure).run()


class Test_Graphics:

    # def test_PlotMaxAndMinAsymetryProcedure(self):
    #     from Walking.WalkingFilters import WalkingKinematicsFilter
    #     from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure

    #     procedure = GroundReactionForceKinematicsProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingKinematicsFilter
    #     from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

    #     procedure = DynamicSymetryFunctionComputeProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()

    #     from Walking.WalkingGraphicsProcedure import PlotMaxAndMinAsymetryProcedure
    #     from Walking.WalkingFilters import WalkingGraphicsFilter

    #     procedure = PlotMaxAndMinAsymetryProcedure()
    #     WalkingGraphicsFilter(walking, procedure).run()

    # def test_PlotWorthAndBestStepProcedure(self):
    #     from Walking.WalkingFilters import WalkingDataProcessingFilter
    #     from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    #     procedure = NormalisationProcedure()
    #     WalkingDataProcessingFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingKinematicsFilter
    #     from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    #     procedure = GroundReactionForceKinematicsProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingKinematicsFilter
    #     from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

    #     procedure = DynamicSymetryFunctionComputeProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingGraphicsFilter
    #     from Walking.WalkingGraphicsProcedure import PlotWorthAndBestStepProcedure
    #     procedure = PlotWorthAndBestStepProcedure()
    #     WalkingGraphicsFilter(walking, procedure).run()

    # def test_PlotCutGroundReactionForceProcedure(self):
    #     from Walking.WalkingFilters import WalkingDataProcessingFilter
    #     from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

    #     procedure = CutDataProcessingProcedure()
    #     procedure.setCutNumber(n_cut=3)
    #     WalkingDataProcessingFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingGraphicsFilter
    #     from Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
        
    #     procedure = PlotCutGroundReactionForceProcedure()
    #     WalkingGraphicsFilter(walking, procedure).run()

    # def test_PlotTwoStepProcedure(self):
    #     from Walking.WalkingFilters import WalkingKinematicsFilter, WalkingGraphicsFilter
    #     from Walking.WalkingKinematicsProcedure import TwoStepProcedure
    #     procedure = TwoStepProcedure()
    #     WalkingKinematicsFilter(walking, procedure).run()

    #     from Walking.WalkingFilters import WalkingGraphicsFilter
    #     from Walking.WalkingGraphicsProcedure import PlotTwoStepProcedure
    #     procedure = PlotTwoStepProcedure()
    #     WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotDynamicSymetryFunctionNormalisedProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()
    
        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure

        procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
        WalkingGraphicsFilter(walking, procedure).run()