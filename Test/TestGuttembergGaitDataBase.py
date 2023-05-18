# pytest -q --disable-pytest-warnings  TestGuttembergGaitDataBase.py

# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_reader::test_ReadMottekc3d

# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Walking::test_Initialisation_Walking

# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Kinematics::test_GroundReactionForceKinematicsProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Kinematics::test_DynamicSymetryFunctionComputeProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Kinematics::test_TwoStepProcedure

# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_DataProcessing::test_NormalisationProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_DataProcessing::test_CutDataProcessingProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_DataProcessing::test_DeleteStepProcedure

# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Graphics::test_PlotMaxAndMinAsymetryProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Graphics::test_PlotWorthAndBestStepProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Graphics::test_PlotCutGroundReactionForceProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Graphics::test_PlotTwoStepProcedure
# pytest -s --disable-pytest-warnings  TestGuttembergGaitDataBase.py::Test_Graphics::test_PlotDynamicSymetryFunctionNormalisedProcedure

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import h5py

""" 
    Choix du patient avec ID 
    Importation des data depuis le fichier h5 créer à partir de la base de données Guttemberg Gait Database (write_h5_GuttembergGaitDatabase)
"""
ID = 1
mass = 60
DataPath = "C:/Users/Nathan/Desktop/Recherche/Github/semelle_connecte/Test/Dataset_test/"
GuttembergGaitDatabase = h5py.File(os.path.join(DataPath, "GuttenbergGaitDatabase.hdf5"), "r")
VerticalGrfLeft = GuttembergGaitDatabase[f"{ID}"]["VerticalGrfLeft"]
ApGrfLeft = GuttembergGaitDatabase[f"{ID}"]["ApGrfLeft"]
MediolateralGrfLeft = GuttembergGaitDatabase[f"{ID}"]["MediolateralGrfLeft"]
VerticalGrfRight = GuttembergGaitDatabase[f"{ID}"]["VerticalGrfRight"]
ApGrfRight = GuttembergGaitDatabase[f"{ID}"]["ApGrfRight"]
MediolateralGrfRight = GuttembergGaitDatabase[f"{ID}"]["MediolateralGrfRight"]


""" Création et implémentation de l'objet Walking avec des semelles """
from SOLE.FeetMe import FeetMe
from Walking.Walking import Walking

dataLeft = pd.DataFrame()
dataLeft["VerticalVGrf"] = VerticalGrfLeft
dataLeft["ApGrf"] = ApGrfLeft
dataLeft["MediolateralGrf"] = MediolateralGrfLeft
dataLeft = dataLeft * 100 # permets de travailler avec des forces de réaction au sol d'un ordre de grandeur de 100

dataRight = pd.DataFrame()
dataRight["VerticalVGrf"] = VerticalGrfRight
dataRight["ApGrf"] = ApGrfRight
dataRight["MediolateralGrf"] = MediolateralGrfRight
dataRight = dataRight * 100 # permets de travailler avec des forces de réaction au sol d'un ordre de grandeur de 100


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