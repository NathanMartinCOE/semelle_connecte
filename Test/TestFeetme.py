# pytest -q --disable-pytest-warnings  TestFeetme.py

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_reader::test_readFeetMeCsv

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_GroundReactionForceKinematicsProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_DynamicSymetryFunctionComputeProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_TwoStepProcedure

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_NormalisationProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_CutDataProcessingProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_DeleteStepProcedure

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotMaxAndMinAsymetryProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotWorthAndBestStepProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotCutGroundReactionForceProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotTwoStepProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotDynamicSymetryFunctionNormalisedProcedure

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Writer::test_Writer

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking
from Tools.ToolsFFT import TransformFourrier


StoragePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\test\\"
FileName = "nathan.csv"
DataPath = os.path.join(StoragePath, FileName)
mass = 60

class Test_reader():

    def test_readFeetMeCsv(self):
        from SOLE.FeetMe import readFeetMeCsv
        SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = DataPath, freq = 10)


from SOLE.FeetMe import readFeetMeCsv
SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = DataPath, freq = 10, show_graph=False, expert=True)

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

        procedure = TwoStepProcedure(firts_step="left")
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
        procedure = TwoStepProcedure(firts_step="left")
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


class Test_Writer:

    def test_Writer(self):
        def RunSomeProcedure(GRFKP = True, DSFCP = True, CDPP = True):
            if GRFKP == True:
                from Walking.WalkingFilters import WalkingKinematicsFilter
                from Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
                procedure = GroundReactionForceKinematicsProcedure()
                WalkingKinematicsFilter(walking, procedure).run()
            if DSFCP == True:
                from Walking.WalkingFilters import WalkingDataProcessingFilter
                from Walking.WalkingDataProcessingProcedure import NormalisationProcedure
                procedure = NormalisationProcedure()
                WalkingDataProcessingFilter(walking, procedure).run()
                from Walking.WalkingFilters import WalkingKinematicsFilter
                from Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
                procedure = DynamicSymetryFunctionComputeProcedure()
                WalkingKinematicsFilter(walking, procedure).run()
            if CDPP == True:
                from Walking.WalkingFilters import WalkingDataProcessingFilter
                from Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure
                procedure = CutDataProcessingProcedure()
                procedure.setCutNumber(n_cut=3)
                WalkingDataProcessingFilter(walking, procedure).run()

        RunSomeProcedure(GRFKP = True, DSFCP = True, CDPP = True)
        from Writer.Writer import Writer
        StoragePath = 'C:\\Users\\Nathan\\Desktop\\Recherche\\Github\\semelle_connecte\\Test\\Dataset_test\\'
        Writer(walking = walking, path = StoragePath, file_name = 'walking_test_Writer_Feetme.hdf5').writeh5()
        
        RunSomeProcedure(GRFKP = False, DSFCP = False, CDPP = False) # do a h5 file without all data
        Writer(walking = walking, path = StoragePath, file_name = 'walking_test_Incomplete_Writer_Feetme.hdf5').writeh5()


