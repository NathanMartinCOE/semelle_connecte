# pytest -q --disable-pytest-warnings  TestMottekGait.py

# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_reader::test_ReadMottekc3d

# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Walking::test_Initialisation_Walking

# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Kinematics::test_GroundReactionForceKinematicsProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Kinematics::test_DynamicSymetryFunctionComputeProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Kinematics::test_TwoStepProcedure

# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_DataProcessing::test_NormalisationProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_DataProcessing::test_CutDataProcessingProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_DataProcessing::test_DeleteStepProcedure

# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Graphics::test_PlotMaxAndMinAsymetryProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Graphics::test_PlotWorthAndBestStepProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Graphics::test_PlotCutGroundReactionForceProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Graphics::test_PlotTwoStepProcedure
# pytest -s --disable-pytest-warnings  TestMottekGait.py::Test_Graphics::test_PlotDynamicSymetryFunctionNormalisedProcedure

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

class Test_reader():
    def test_ReadMottekc3d(self):
        from Reader.MottekReader import ReadMottekc3d
        dataLeft, dataRight = ReadMottekc3d(Path, mass=60)

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
        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

    def test_DynamicSymetryFunctionComputeProcedure(self):
        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
    
    def test_TwoStepProcedure(self):
        from Walking.WalkingFilters import WalkingKinematicsFilter, WalkingGraphicsFilter
        from Walking.WalkingKinematicsProcedure import TwoStepProcedure

        procedure = TwoStepProcedure()
        WalkingKinematicsFilter(walking, procedure).run()


class Test_DataProcessing:

    def test_NormalisationProcedure(self):
        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure

        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

    def test_CutDataProcessingProcedure(self):

        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

        procedure = CutDataProcessingProcedure()
        procedure.setCutNumber(n_cut=3)
        WalkingDataProcessingFilter(walking, procedure).run()
    
    def test_DeleteStepProcedure(self):
        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import DeleteStepProcedure
        procedure = DeleteStepProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()


class Test_Graphics:

    def test_PlotMaxAndMinAsymetryProcedure(self):
        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingGraphicsProcedure import PlotMaxAndMinAsymetryProcedure
        from Walking.WalkingFilters import WalkingGraphicsFilter

        procedure = PlotMaxAndMinAsymetryProcedure()
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotWorthAndBestStepProcedure(self):
        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingGraphicsFilter
        from Walking.WalkingGraphicsProcedure import PlotWorthAndBestStepProcedure
        procedure = PlotWorthAndBestStepProcedure()
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotCutGroundReactionForceProcedure(self):
        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

        procedure = CutDataProcessingProcedure()
        procedure.setCutNumber(n_cut=3)
        WalkingDataProcessingFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingGraphicsFilter
        from Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
        
        procedure = PlotCutGroundReactionForceProcedure()
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotTwoStepProcedure(self):
        from Walking.WalkingFilters import WalkingKinematicsFilter, WalkingGraphicsFilter
        from Walking.WalkingKinematicsProcedure import TwoStepProcedure
        procedure = TwoStepProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingGraphicsFilter
        from Walking.WalkingGraphicsProcedure import PlotTwoStepProcedure
        procedure = PlotTwoStepProcedure()
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotDynamicSymetryFunctionNormalisedProcedure(self):
        from Walking.WalkingFilters import WalkingKinematicsFilter
        from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingDataProcessingFilter
        from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from Walking.WalkingFilters import WalkingGraphicsFilter
        from Walking.WalkingGraphicsProcedure import PlotDynamicSymetryFunctionNormalisedProcedure

        procedure = PlotDynamicSymetryFunctionNormalisedProcedure()
        WalkingGraphicsFilter(walking, procedure).run()