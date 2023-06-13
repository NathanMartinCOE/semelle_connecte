import pandas as pd
import os
import h5py
from tqdm import tqdm
import numpy as np

datasetR_m1 = pd.DataFrame()
datasetR_m2 = pd.DataFrame()

for ID in tqdm(np.arange(1,350)):
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
    from semelle_connecte.SOLE.FeetMe import FeetMe
    from semelle_connecte.Walking.Walking import Walking

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


    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import GroundReactionForceKinematicsProcedure
    procedure = GroundReactionForceKinematicsProcedure()
    WalkingKinematicsFilter(walking, procedure).run()

    from semelle_connecte.Walking.WalkingFilters import WalkingDataProcessingFilter
    from semelle_connecte.Walking.WalkingDataProcessingProcedure import NormalisationProcedure
    procedure = NormalisationProcedure()
    WalkingDataProcessingFilter(walking, procedure).run()

    from semelle_connecte.Walking.WalkingFilters import WalkingKinematicsFilter
    from semelle_connecte.Walking.WalkingKinematicsProcedure import DynamicSymetryFunctionComputeProcedure
    procedure = DynamicSymetryFunctionComputeProcedure()
    WalkingKinematicsFilter(walking, procedure).run()
    
    df_FSD = walking.m_DataFrameDynamicSymetryScore
    df_FSD["ID"] = ID
    df_FSD_m1 = df_FSD[0:50]
    df_FSD_m2 = df_FSD[50:100]
    if ID == 1:
        datasetR_m1 = df_FSD_m1
        datasetR_m2 = df_FSD_m2
    if ID != 1:
        datasetR_m1 = pd.concat([datasetR_m1, df_FSD_m1], ignore_index = True)
        datasetR_m2 = pd.concat([datasetR_m2, df_FSD_m2], ignore_index = True)


datasetR_m1.to_csv("C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\datasetR_m1.csv")
datasetR_m2.to_csv("C:\\Users\\Nathan\\Desktop\\Recherche\\R_studio\\datasetR_m2.csv")