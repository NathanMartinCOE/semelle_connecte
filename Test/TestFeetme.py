# pytest -q --disable-pytest-warnings  TestFeetme.py

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_reader::test_readFeetMeCsv
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_reader::test_readFeetMeMultipleCsv
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_reader::test_ReadSpatioTemporalCsv

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_GroundReactionForceKinematicsProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_DynamicSymetryFunctionComputeProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Kinematics::test_TwoStepProcedure

####### pytest -s --disable-pytest-warnings  TestFeetme.py::Test_SpatioTemporal::test_SpatioTemporalGaitCycle

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_NormalisationProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_CutDataProcessingProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_DataProcessing::test_DeleteStepProcedure

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotMaxAndMinAsymetryProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotWorthAndBestStepProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotCutGroundReactionForceProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotTwoStepProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotDynamicSymetryFunctionNormalisedProcedure
# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Graphics::test_PlotVerticalGroundReaction3DProcedure

# pytest -s --disable-pytest-warnings  TestFeetme.py::Test_Writer::test_Writer

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

from pyCGM2.Tools import btkTools
from pyCGM2.ForcePlates import forceplates

from semelle_connecte.SOLE.FeetMe import FeetMe
from semelle_connecte.Walking.Walking import Walking
from semelle_connecte.Tools.ToolsFFT import TransformFourrier


StoragePath = "C:\\Users\\Nathan\\Desktop\\Wheelchair tests datas\\FeetMe\\test\\"
FileName = "nathan.csv"
DataPath = os.path.join(StoragePath, FileName)
mass = 60

class Test_reader():

    def test_readFeetMeCsv(self):
        from semelle_connecte.SOLE.FeetMe import readFeetMeCsv
        SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = DataPath, freq = 110)

    def test_readFeetMeMultipleCsv(self):
        from semelle_connecte.SOLE.FeetMe import readFeetMeMultipleCsv
        file_names = ["nathan_TDM_1.csv", "nathan_TDM_2.csv", "nathan_TDM_3.csv", "nathan_TDM_4.csv"]
        fullfilenames = []
        for file_name in file_names:
            fullfilenames.append(os.path.join(StoragePath, file_name))
        SoleInstanceRight, SoleInstanceLeft = readFeetMeMultipleCsv(fullfilenames = fullfilenames, freq = 110)
    
    def test_ReadSpatioTemporalCsv(self):
        from semelle_connecte.SOLE.FeetMe import ReadSpatioTemporalCsv
        file_name = "Nathan_R_metrics.csv"
        fullfilename = os.path.join(StoragePath, file_name) 
        DataFrameSpatioTemporal = ReadSpatioTemporalCsv(fullfilename)


from semelle_connecte.SOLE.FeetMe import readFeetMeCsv
SoleInstanceRight, SoleInstanceLeft = readFeetMeCsv(fullfilename = DataPath, freq = 10, show_graph=False, expert=True)

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
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()
    
    def test_TwoStepProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter, WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import TwoStepProcedure

        procedure = TwoStepProcedure(firts_step="left")
        WalkingKinematicsFilter(walking, procedure).run()



from semelle_connecte.SOLE.FeetMe import ReadSpatioTemporalCsv
DataFrameSpatioTemporal_Left, DataFrameSpatioTemporal_Right = ReadSpatioTemporalCsv(os.path.join(StoragePath, "Nathan_R_metrics.csv") )

walking.setDataFrameSpatioTemporal_Left(DataFrameSpatioTemporal_Left)
walking.setDataFrameSpatioTemporal_Right(DataFrameSpatioTemporal_Right)


class Test_SpatioTemporal:

    def test_SpatioTemporalGaitCycle(self):
        from semelle_connecte.Walking.WalkingSpatioTemporalProcedure import SpatioTemporalGaitCycleProcedure
        from semelle_connecte.Walking.WalkingFilters import WalkingSpatioTemporalFilter
        procedure = SpatioTemporalGaitCycleProcedure()
        WalkingSpatioTemporalFilter(walking, procedure).run() 



class Test_DataProcessing:

    def test_NormalisationProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure

        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

    def test_CutDataProcessingProcedure(self):

        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

        procedure = CutDataProcessingProcedure()
        procedure.setCutNumber(n_cut=3)
        WalkingDataProcessingFilter(walking, procedure).run()
    
    def test_DeleteStepProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import DeleteStepProcedure
        procedure = DeleteStepProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()


class Test_Graphics:

    def test_PlotMaxAndMinAsymetryProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotMaxAndMinAsymetryProcedure
        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter

        procedure = PlotMaxAndMinAsymetryProcedure(show_graph = False)
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotWorthAndBestStepProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure

        procedure = DynamicSymetryFunctionComputeProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotWorthAndBestStepProcedure
        procedure = PlotWorthAndBestStepProcedure(show_graph = False)
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotCutGroundReactionForceProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure

        procedure = CutDataProcessingProcedure()
        procedure.setCutNumber(n_cut=3)
        WalkingDataProcessingFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotCutGroundReactionForceProcedure
        
        procedure = PlotCutGroundReactionForceProcedure(show_graph = False)
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotTwoStepProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter, WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import TwoStepProcedure
        procedure = TwoStepProcedure(firts_step="left")
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotTwoStepProcedure
        procedure = PlotTwoStepProcedure(show_graph = False)
        WalkingGraphicsFilter(walking, procedure).run()

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

        procedure = PlotDynamicSymetryFunctionNormalisedProcedure(show_graph = False)
        WalkingGraphicsFilter(walking, procedure).run()

    def test_PlotVerticalGroundReaction3DProcedure(self):
        from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
        from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
        procedure = GroundReactionForceKinematicsProcedure()
        WalkingKinematicsFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
        from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
        procedure = NormalisationProcedure()
        WalkingDataProcessingFilter(walking, procedure).run()

        from semelle_connecte.Walking.WalkingFilters import WalkingGraphicsFilter
        from semelle_connecte.Walking.WalkingGraphicsProcedure import PlotVerticalGroundReaction3DProcedure

        procedure = PlotVerticalGroundReaction3DProcedure(show_graph = True)
        WalkingGraphicsFilter(walking, procedure).run()



class Test_Writer:

    def test_Writer(self):
        def RunSomeProcedure(GRFKP = True, DSFCP = True, CDPP = True):
            if GRFKP == True:
                from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
                from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
                procedure = GroundReactionForceKinematicsProcedure()
                WalkingKinematicsFilter(walking, procedure).run()
            if DSFCP == True:
                from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
                from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
                procedure = NormalisationProcedure()
                WalkingDataProcessingFilter(walking, procedure).run()
                from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
                from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
                procedure = DynamicSymetryFunctionComputeProcedure()
                WalkingKinematicsFilter(walking, procedure).run()
            if CDPP == True:
                from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
                from semelle_connecte.Walking.WalkingDataProcessingProcedure import CutDataProcessingProcedure
                procedure = CutDataProcessingProcedure()
                procedure.setCutNumber(n_cut=3)
                WalkingDataProcessingFilter(walking, procedure).run()

        RunSomeProcedure(GRFKP = True, DSFCP = True, CDPP = True)
        from semelle_connecte.Writer.Writer import Writer
        import semelle_connecte
        StoragePath = os.path.join(semelle_connecte.Connected_Insole_Path, 'semelle_connecte\\Test\\Dataset_test\\')
        Writer(walking = walking, path = StoragePath, file_name = 'walking_test_Writer_Feetme.hdf5').writeh5()
        
        RunSomeProcedure(GRFKP = False, DSFCP = False, CDPP = False) # do a h5 file without all data
        Writer(walking = walking, path = StoragePath, file_name = 'walking_test_Incomplete_Writer_Feetme.hdf5').writeh5()


